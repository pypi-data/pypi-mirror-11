# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for `lino_welfare.modlib.isip`.

"""

from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from atelier.utils import AttrDict

from lino.api import dd, rt
from lino import mixins

from lino.modlib.excerpts.mixins import Certifiable
from lino.modlib.cal.mixins import EventGenerator
from lino.modlib.contacts.mixins import ContactRelated
from lino.modlib.cal.utils import DurationUnits, update_auto_task
# from lino.modlib.system.mixins import PeriodEvents

from lino.utils.ranges import isrange
from lino.utils.ranges import overlap2, encompass
from lino.mixins.periods import rangefmt

from lino_welfare.modlib.system.models import Signers
from lino_welfare.modlib.pcsw.models import ClientChecker
from lino_welfare.modlib.integ.roles import IntegrationAgent

from .choicelists import ContractEvents, OverlapGroups


def default_signer1():
    return settings.SITE.site_config.signer1


def default_signer2():
    return settings.SITE.site_config.signer2


class ContractTypeBase(mixins.BabelNamed):
    """Base class for all `ContractType` models.

    .. attribute:: full_name

        The full description of this contract type as used in printed
        documents.

    .. attribute:: exam_policy

        The default examination policy to be used for contracts of
        this type.

        This is a pointer to :class:`ExamPolicy
        <lino_welfare.modlib.isip.models.ExamPolicy>`. All contract
        types share the same set of examination policies.

    .. attribute:: overlap_group

        The overlap group to use when checking whether two contracts
        are overlapping or not. See :class:`OverlappingContractsTest`.
        If this field is empty, Lino does not check at all for
        overlapping contracts.

    .. attribute:: template

        The main template to use instead of the default template
        defined on the excerpt type.
    
        See
        :meth:`lino.modlib.excerpts.mixins.Certifiable.get_excerpt_templates`.

    """

    class Meta:
        abstract = True

    full_name = models.CharField(_("Full name"), blank=True, max_length=200)

    exam_policy = dd.ForeignKey(
        "isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)

    overlap_group = OverlapGroups.field(blank=True)
    template = models.CharField(_("Template"), max_length=200, blank=True)

    @dd.chooser(simple_values=True)
    def template_choices(cls):
        bm = rt.modules.printing.BuildMethods.get_system_default()
        return rt.find_template_config_files(
            bm.template_ext, cls.templates_group)


class ContractPartnerBase(ContactRelated):
    class Meta:
        abstract = True

    def get_recipient(self):
        contact = self.get_contact()
        if contact is not None:
            return contact
        if self.company:
            return self.company
        return self.client
    recipient = property(get_recipient)

    @classmethod
    def contact_person_choices_queryset(cls, company):
        return rt.modules.contacts.Person.objects.filter(
            rolesbyperson__company=company,
            rolesbyperson__type__use_in_contracts=True)

    @dd.chooser()
    def contact_role_choices(cls):
        return rt.modules.contacts.RoleType.objects.filter(
            use_in_contracts=True)


class OverlappingContractsTest:
    """Volatile object used to test for overlapping contracts.  It is
    responsible for issuing the following error messages:

    - :message:`Date range overlaps with X #Y` means that the date
      periods of two contracts of the same client and the same overlap
      group (see :class:`OverlapGroups`) overlap.

    - (Currently deactivated) Date range X lies outside of coached period (Y)

    """

    def __init__(self, client):
        self.client = client
        self.actives = []
        for model in rt.models_by_base(ContractBase):
            for con1 in model.objects.filter(client=client):
                ap = con1.active_period()
                if ap[0] is None and ap[1] is None:
                    continue
                self.actives.append((ap, con1))

    def check(self, con1):
        ap = con1.active_period()
        if ap[0] is None and ap[1] is None:
            return
        if False:
            cp = (self.client.coached_from, self.client.coached_until)
            if not encompass(cp, ap):
                return _("Date range %(p1)s lies outside of coached "
                         "period %(p2)s.") \
                    % dict(p2=rangefmt(cp), p1=rangefmt(ap))
        for (p2, con2) in self.actives:
            if con1 != con2 and overlap2(ap, p2):
                if con1.type.overlap_group == con2.type.overlap_group:
                    msg = _("Date range overlaps with {ctype} #{id}.")
                    msg = msg.format(
                        ctype=con2.__class__._meta.verbose_name,
                        id=con2.pk)
                    return msg
        return None

    def check_all(self):
        messages = []
        for (p1, con1) in self.actives:
            msg = self.check(con1)
            if msg:
                messages.append(
                    _("%(ctype)s #%(id)s : %(msg)s") % dict(
                        msg=msg,
                        ctype=con1.__class__._meta.verbose_name,
                        id=con1.pk))
        return messages


class OverlappingContractsChecker(ClientChecker):
    """A given client cannot have two active contracts at the same time.

    """
    verbose_name = _("Check for overlapping contracts")

    def get_plausibility_problems(self, obj, fix=False):
        msg = '  '.join(OverlappingContractsTest(obj).check_all())
        if msg:
            yield (False, msg)

OverlappingContractsChecker.activate()


class ContractBase(Signers, Certifiable, EventGenerator):
    """Abstract base class for all *integration contracts* (an unofficial
    term), i.e.  :class:`isip.Contract
    <lino_welfare.modlib.isip.models.Contract>` :class:`jobs.Contract
    <lino_welfare.modlib.jobs.models.Contract>` and
    :class:`immersions.Contract
    <lino_welfare.modlib.immersions.models.Contract>`

    .. attribute:: client

        The client for whom this contract is done.

    .. attribute:: applies_from

        The start date of the contract.
    
    .. attribute:: applies_until

        The planned end date.
    
    .. attribute:: date_ended

        The date when this contract was prematuredly ended. When
        nonempty, the :attr:`ended` field should also be filled.  This field
        is usually empty.

    .. attribute:: ending

        The reason of prematured ending.  Pointer to
        :class:`ContractEnding
        <lino_welfare.modlib.isip.choicelists.ContractEnding>`

    .. attribute:: date_decided
    .. attribute:: language

        The language of this contract. Default value is the client's
        :attr:`language<lino_welfare.modlib.pcw.models.Client.language>`.

    .. attribute:: type

        The type of this contract. Pointer to a subclass of
        :class:`ContractTypeBase`.

    """

    manager_roles_required = dd.login_required(IntegrationAgent)

    TASKTYPE_CONTRACT_APPLIES_UNTIL = 1

    class Meta:
        abstract = True

    client = models.ForeignKey(
        'pcsw.Client',
        related_name="%(app_label)s_%(class)s_set_by_client")

    language = dd.LanguageField()

    applies_from = models.DateField(_("applies from"), blank=True, null=True)
    applies_until = models.DateField(_("applies until"), blank=True, null=True)
    date_decided = models.DateField(
        blank=True, null=True, verbose_name=_("date decided"))
    date_issued = models.DateField(
        blank=True, null=True, verbose_name=_("date issued"))

    user_asd = models.ForeignKey(
        "users.User",
        verbose_name=_("responsible (ASD)"),
        related_name="%(app_label)s_%(class)s_set_by_user_asd",
        #~ related_name='contracts_asd',
        blank=True, null=True)

    exam_policy = models.ForeignKey(
        "isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)

    ending = models.ForeignKey(
        "isip.ContractEnding",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)
    date_ended = models.DateField(
        blank=True, null=True, verbose_name=_("date ended"))

    # hidden_columns = 'date_decided date_issued \
    # exam_policy user_asd ending date_ended signer1 signer2'

    def __unicode__(self):
        kw = dict(type=unicode(self._meta.verbose_name))
        if self.pk is None:
            kw.update(client=unicode(self.client))
            return '{type} ({client})'.format(**kw)
        kw.update(
            id=self.pk,
            client=self.client.get_full_name(salutation=False))
        return '{type}#{id} ({client})'.format(**kw)
        # return u'%s#%s (%s)' % (self._meta.verbose_name, self.pk,
        #                         self.client.get_full_name(salutation=False))

    def get_excerpt_title(self):
        """The printed title of a contract specifies just the contract type
        (not the number and name of client).

        """
        return unicode(self.type)
        # return unicode(self._meta.verbose_name)

    def get_excerpt_templates(self, bm):
        """Overrides
        :meth:`lino.modlib.excerpts.mixins.Certifiable.get_excerpt_templates`.

        """
        if self.type_id:
            if self.type.template:
                # assert self.type.template.endswith(bm.template_ext)
                return [self.type.template]
        
    # backwards compat for document templates
    def get_person(self):
        return self.client
    person = property(get_person)

    def get_print_language(self):
        return self.language

    @dd.chooser()
    def ending_choices(cls):
        return rt.modules.isip.ContractEnding.objects.filter(use_in_isip=True)

    def client_changed(self, ar):

        """If the contract's author is the client's primary coach, then set
        user_asd to None, otherwise set user_asd to the primary coach.
        We suppose that only integration agents write contracts.
        """

        if self.client_id is not None:
            #~ pc = self.person.get_primary_coach()
            #~ qs = self.person.get_coachings(self.applies_from,active=True)
            qs = self.client.get_coachings(
                (self.applies_from, self.applies_until),
                type__does_gss=True)
            if qs.count() == 1:
                user_asd = qs[0].user
                if user_asd is None or user_asd == self.user:
                    self.user_asd = None
                else:
                    self.user_asd = user_asd
                
    def on_create(self, ar):
        super(ContractBase, self).on_create(ar)
        self.client_changed(ar)

    def after_ui_save(self, ar, cw):
        super(ContractBase, self).after_ui_save(ar, cw)
        self.update_reminders(ar)

    def full_clean(self, *args, **kw):
        """Checks for the following error conditions:

- You must specify a contract type.
- :message:`Contract ends before it started.`
- Any error message returned by :class:`OverlappingContractsTest`

"""
        r = self.active_period()
        if not isrange(*r):
            raise ValidationError(_('Contract ends before it started.'))

        if self.type_id:
            if not self.exam_policy_id:
                if self.type.exam_policy_id:
                    self.exam_policy_id = self.type.exam_policy_id

            if self.client_id is not None:
                if self.type.overlap_group:
                    msg = OverlappingContractsTest(self.client).check(self)
                    if msg:
                        raise ValidationError(msg)
        super(ContractBase, self).full_clean(*args, **kw)

        if self.type_id is None:
            raise ValidationError(dict(
                type=[_("You must specify a contract type.")]))

    def update_owned_instance(self, other):
        if isinstance(other, mixins.ProjectRelated):
            other.project = self.client
        super(ContractBase, self).update_owned_instance(other)

    def setup_auto_event(self, evt):
        """This implements the rule that suggested evaluation events should
        be for the *currently responsible* coach, which may differ from
        the contract's author. This is relevant if coach changes while
        contract is active (see :doc:`/specs/integ`).

        The **currently responsible coach** is the user for which
        there is a coaching which has :attr:`does_integ
        <lino_welfare.modlib.pcsw.coaching.CoachingType.does_integ>`
        set to `True`..

        """
        super(ContractBase, self).setup_auto_event(evt)
        d = evt.start_date
        coachings = evt.owner.client.get_coachings(
            (d, d), type__does_integ=True)
        if coachings.count() == 1:
            evt.user = coachings[0].user

    def update_cal_rset(self):
        return self.exam_policy

    def update_cal_from(self, ar):
        date = self.applies_from
        if not date:
            return None
        rset = self.update_cal_rset()
        return rset.get_next_suggested_date(ar, date)

    def update_cal_calendar(self):
        if self.exam_policy is not None:
            return self.exam_policy.event_type

    def update_cal_until(self):
        return self.date_ended or self.applies_until

    def update_cal_summary(self, i):
        ep = self.exam_policy
        if ep is not None and ep.event_type is not None:
            if ep.event_type.event_label:
                return ep.event_type.event_label + " " + str(i)
        return _("Evaluation %d") % i

    def update_reminders(self, ar):
        rv = super(ContractBase, self).update_reminders(ar)
        au = self.update_cal_until()
        if au:
            au = DurationUnits.months.add_duration(au, -1)
        update_auto_task(
            self.TASKTYPE_CONTRACT_APPLIES_UNTIL,
            self.user,
            au,
            _("Contract ends in a month"),
            self)
        return rv

    def active_period(self):
        return (self.applies_from, self.date_ended or self.applies_until)

    def get_granting(self, **aidtype_filter):
        ap = self.active_period()
        ap = AttrDict(start_date=ap[0], end_date=ap[1])
        return rt.modules.aids.Granting.objects.get_by_aidtype(
            self.client, ap, **aidtype_filter)

    def get_aid_type(self):
        # may be used in `.odt` template for `isip.Contract`
        g = self.get_granting(is_integ_duty=True)
        if g is not None:
            return g.aid_type

    def get_aid_confirmation(self):
        """Returns the last aid confirmation that has been issued for this
        contract. May be used in `.odt` template.

        """
        g = self.get_granting(is_integ_duty=True)
        if g and g.aid_type and g.aid_type.confirmation_type:
            ct = g.aid_type.confirmation_type
            qs = ct.model.objects.filter(granting=g)
            # ap = self.active_period()
            # ap = AttrDict(start_date=ap[0], end_date=ap[1])
            # qs = PeriodEvents.active.add_filter(qs, ap)
            if qs.count() > 0:
                return qs[qs.count()-1]

    def suggest_cal_guests(self, event):
        """Automatic evaluation events have the client as mandatory
        participant, plus possibly some other coach.

        """
        client = event.project
        if client is None:
            return
        Guest = rt.modules.cal.Guest
        # GuestStates = rt.modules.cal.GuestStates
        # st = GuestStates.accepted
        # yield Guest(event=event,
        #             partner=client,
        #             state=st,
        #             role=settings.SITE.site_config.client_guestrole)

        period = (event.start_date, event.start_date)
        qs = client.get_coachings(period)
        qs = client.get_coachings(period, user__partner__isnull=False)
        for coaching in qs:
            if coaching.type and coaching.type.eval_guestrole:
                u = coaching.user
                if u != event.user and u.partner is not None:
                    yield Guest(event=event,
                                partner=u.partner,
                                role=coaching.type.eval_guestrole)

dd.update_field(ContractBase, 'signer1', default=default_signer1)
dd.update_field(ContractBase, 'signer2', default=default_signer2)


class ContractBaseTable(dd.Table):
    """Base for contract tables. Defines the following parameter fields:

    .. attribute:: user
    .. attribute:: observed_event

    .. attribute:: ending

        Show only contracts with the specified
        :class:`ContractEnding
        <lino_welfare.modlib.isip.models.ContractEnding>`.

    .. attribute:: ending_success

        Select "Yes" to show only contracts whose ending
        :class:`ContractEnding
        <lino_welfare.modlib.isip.models.ContractEnding>` has
        :attr:`is_success
        <lino_welfare.modlib.isip.models.ContractEnding.is_success>`
        checked.

    """
    parameters = mixins.ObservedPeriod(
        user=dd.ForeignKey(settings.SITE.user_model, blank=True),

        observed_event=ContractEvents.field(
            blank=True, default=ContractEvents.active),

        ending_success=dd.YesNo.field(
            _("Successfully ended"),
            blank=True,
            help_text="""Contrats terminés avec succès."""),
        ending=models.ForeignKey(
            'isip.ContractEnding',
            blank=True, null=True,
            help_text="""Nur Konventionen mit diesem Beendigungsgrund."""),
        company=models.ForeignKey(
            'contacts.Company',
            blank=True, null=True,
            help_text=_("Only contracts with this company as partner."))
    )

    params_layout = """
    user type start_date end_date observed_event
    company ending_success ending
    """
    params_panel_hidden = True

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(ContractBaseTable, cls).get_request_queryset(ar)
        pv = ar.param_values
        #~ logger.info("20120608.get_request_queryset param_values = %r", pv)
        if pv.user:
            qs = qs.filter(user=pv.user)
        if pv.type:
            qs = qs.filter(type=pv.type)

        ce = pv.observed_event
        if pv.start_date is None or pv.end_date is None:
            period = None
        else:
            period = (pv.start_date, pv.end_date)
        if ce and period is not None:
            if ce == ContractEvents.ended:
                qs = qs.filter(dd.inrange_filter('applies_until', period)
                               | dd.inrange_filter('date_ended', period))
            elif ce == ContractEvents.started:
                qs = qs.filter(dd.inrange_filter('applies_from', period))
            elif ce == ContractEvents.signed:
                qs = qs.filter(dd.inrange_filter('date_decided', period))
            elif ce == ContractEvents.active:
                f1 = Q(applies_until__isnull=True) | Q(
                    applies_until__gte=period[0])
                flt = f1 & (Q(date_ended__isnull=True) |
                            Q(date_ended__gte=period[0]))
                flt &= Q(applies_from__lte=period[1])
                qs = qs.filter(flt)
            else:
                raise Exception(repr(ce))

        if pv.ending_success == dd.YesNo.yes:
            qs = qs.filter(ending__isnull=False, ending__is_success=True)
        elif pv.ending_success == dd.YesNo.no:
            qs = qs.filter(ending__isnull=False, ending__is_success=False)

        if pv.ending is not None:
            qs = qs.filter(ending=pv.ending)
        #~ logger.info("20130524 %s",qs.query)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(ContractBaseTable, self).get_title_tags(ar):
            yield t

        pv = ar.param_values
        if pv.start_date is None or pv.end_date is None:
            pass
        else:
            oe = pv.observed_event
            if oe is not None:
                yield "%s %s-%s" % (unicode(oe.text),
                                    dd.dtos(pv.start_date),
                                    dd.dtos(pv.end_date))

        if pv.company:
            yield unicode(pv.company)


