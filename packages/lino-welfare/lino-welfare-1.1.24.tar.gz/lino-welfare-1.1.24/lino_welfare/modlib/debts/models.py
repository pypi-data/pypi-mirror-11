# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino_welfare.modlib.debts`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import decimal

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode

from lino.api import dd, rt, _, pgettext
from lino.utils.xmlgen.html import E
from lino import mixins

from lino.modlib.accounts.choicelists import AccountTypes, AccountCharts
from lino.modlib.excerpts.mixins import Certifiable
from lino.modlib.users.mixins import UserAuthored


from .fields import PeriodsField
from .mixins import SequencedBudgetComponent, ActorBase, MainActor
from .choicelists import TableLayouts

from django.db import transaction


@transaction.commit_on_success
def bulk_create_with_manual_ids(model, obj_list):
    """
    Originally copied from http://stackoverflow.com/a/13143062/407239
    
    """
    last = model.objects.all().aggregate(models.Max('id'))['id__max']
    if last is None:
        id_start = 1
    else:
        id_start = last + 1
    for i, obj in enumerate(obj_list):
        obj.id = id_start + i
    #~ print 20130508, [dd.obj2str(o) for o in obj_list]
    return model.objects.bulk_create(obj_list)


class Budget(UserAuthored, Certifiable, mixins.Duplicable):
    """A document which expresses the financial situation of a partner at
    a given date.

    """

    class Meta:
        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")

    quick_search_fields = ['partner__name']

    date = models.DateField(
        _("Date"), blank=True,
        default=settings.SITE.today)
    partner = models.ForeignKey('contacts.Partner')
    print_todos = models.BooleanField(
        _("Print to-do list"),
        default=False,
        help_text=_("""\
Einträge im Feld "To-do" werden nur ausgedruckt, 
wenn die Option "To-dos drucken" des Budgets angekreuzt ist. 
Diese Option wird aber momentan noch ignoriert 
(d.h. To-do-Liste wird gar nicht ausgedruckt), 
weil wir noch überlegen müssen, *wie* sie ausgedruckt werden sollen. 
Vielleicht mit Fußnoten?"""))
    print_empty_rows = models.BooleanField(
        _("Print empty rows"),
        default=False,
        help_text=_("""Check this to print also empty rows for later completion."""))
    #~ ignore_yearly_incomes = models.BooleanField(
        #~ verbose_name=_("Ignore yearly incomes"),
        #~ help_text=_("""Check this to ignore yearly incomes in the :ref:`welfare.debts.DebtsByBudget`."""))
    include_yearly_incomes = models.BooleanField(
        _("Include yearly incomes"),
        default=False,
        help_text=_("""Check this to include yearly incomes in the Debts Overview table of this Budget."""))
    intro = dd.RichTextField(_("Introduction"), format="html", blank=True)
    conclusion = dd.RichTextField(_("Conclusion"), format="html", blank=True)
    dist_amount = dd.PriceField(_("Distributable amount"), default=120,
        help_text=_("""\
The total monthly amount available for debts distribution."""))

    #~ def duplicated_fields(self):
        #~ return dd.fields_list('partner print_todo intro conclusion dist_amount')

    #~ duplicated_fields = """partner print_todos intro
    #~ conclusion dist_amount actor_set entry_set"""

    def __unicode__(self):
        if self.pk is None:
            return unicode(_("New")) + ' ' + unicode(self._meta.verbose_name)
        return force_unicode(
            _("Budget %(pk)d for %(partner)s")
            % dict(pk=self.pk, partner=self.partner))

    @classmethod
    def get_certifiable_fields(cls):
        return """date partner user intro
        dist_amount include_yearly_incomes
        print_empty_rows print_todos"""

    def get_actors(self):
        """Return a list of the actors of this budget."""
        attname = "_cached_actors"
        if hasattr(self, attname):
            return getattr(self, attname)
        l = list(self.actor_set.all())
        if len(l) > 0:
            main_header = _("Common")
        else:
            main_header = _("Amount")
        l.insert(0, MainActor(self, main_header))
        setattr(self, attname, l)
        return l

    def get_actor_index(self, actor):
        for i, a in enumerate(self.get_actors()):
            if actor == a:
                return i
        raise Exception("No actor '%s' in %s" % (actor, self))

    def get_actor(self, n):
        l = self.get_actors()
        if len(l) > n:
            return l[n]
        else:
            return None

    def get_print_language(self):
        if self.partner:
            return self.partner.language
        return super(Budget, self).get_print_language()

    @property
    def actor1(self):
        return self.get_actor(0)

    @property
    def actor2(self):
        return self.get_actor(1)

    @property
    def actor3(self):
        return self.get_actor(2)

    def entry_groups(self, ar, types=None, **kw):
        """Yield the **entry groups** for this budget, i.e. one item for each
        account group for which this budget has some data.

        :types: an optional string specifying a set of one-letter
                account type names. See :class:`AccountTypes
                <lino.modlib.accounts.choicelists.AccountTypes>`.

        Each entry group is encapsulated as a volatile helper object
        :class:`lino_welfare.modlib.debts.ui.EntryGroup`.

        """
        Group = rt.modules.accounts.Group
        kw.update(chart=AccountCharts.debts)
        kw.update(entries_layout__gt='')
        if types is not None:
            kw.update(
                account_type__in=[AccountTypes.items_dict[t] for t in types])
        for g in Group.objects.filter(**kw).order_by('ref'):
            eg = EntryGroup(self, g, ar)
            if eg.has_data():
                yield eg

    def unused_account_groups(self, types=None, **kw):
        """Yield all AccountGroups which have at least one entry in this
        Budget.

        Parameters:

            types: an optional string specifying a set of one-letter
                   account type names. See :class: `AccountTypes
                   <lino.modlib.accounts.choicelists.AccountTypes>`.

        """
        if types is not None:
            kw.update(account_type__in=[AccountTypes.items_dict[t]
                      for t in types])
        Group = rt.modules.accounts.Group
        for g in Group.objects.filter(**kw).order_by('ref'):
            if Entry.objects.filter(budget=self, account__group=g).count():
                yield g

    def unused_entries_by_group(self, ar, group, **kw):
        """Return a TableRequest showing the entries of this budget for the
        given `group`, using the table layout depending on
        AccountType.

        Parameters:
 
            ar: the ActionRequest

            group: an instance of :class:`accounts.Group <lino.modlib.accounts.models.Group>`.

        """
        t = entries_table_for_group(group)
        #~ print '20130327 entries_by_group', self, t
        if t is None:
            return None
        ar = ar.spawn(t,
                      master_instance=self,
                      title=unicode(group),
                      filter=models.Q(account__group=group), **kw)

        #~ print 20120606, sar
        return ar

    def sum(self, fldname, types=None, exclude=None, *args, **kw):
        """Compute and return the sum of `fldname` (either ``amount`` or
        `monthly_rate`

        """
        fldnames = [fldname]
        if types is not None:
            kw.update(account_type__in=[AccountTypes.items_dict[t]
                      for t in types])
        rv = decimal.Decimal(0)
        kw.update(budget=self)
        qs = Entry.objects.filter(*args, **kw)
        if exclude is not None:
            qs = qs.exclude(**exclude)
        for e in qs.annotate(models.Sum(fldname)):
            amount = decimal.Decimal(0)
            for n in fldnames:
                a = getattr(e, n + '__sum', None)
                if a is not None:
                    amount += a
            if e.periods != 1:
                amount = amount / decimal.Decimal(e.periods)
            rv += amount
        return rv

    def after_ui_save(self, ar, cw):
        """
        Called after successful save()
        """
        self.fill_defaults(ar)

    def fill_defaults(self, ar=None):
        """
        If the budget is empty, fill it with default entries
        by copying the master_budget.
        """
        Entry = rt.modules.debts.Entry
        Actor = rt.modules.debts.Actor
        Account = rt.modules.accounts.Account
        #~ if self.closed:
        if not self.partner or self.printed_by is not None:
            return
        if self.entry_set.all().count() > 0:
            return
        self.save()
        entries = []
        master_budget = settings.SITE.site_config.master_budget
        if master_budget is None:
            flt = models.Q(required_for_household=True)
            flt = flt | models.Q(required_for_person=True)
            seqno = 0
            for acc in Account.objects.filter(flt).order_by('ref'):
                seqno += 1
                e = Entry(account=acc, budget=self,
                          seqno=seqno, account_type=acc.type)
                e.account_changed(ar)
                #~ e.periods = e.account.periods
                if e.account.default_amount:
                    e.amount = e.account.default_amount
                entries.append(e)
        else:
            for me in master_budget.entry_set.order_by(
                    'seqno').select_related():
                e = Entry(account=me.account, budget=self,
                          account_type=me.account_type,
                          seqno=me.seqno, periods=me.periods,
                          amount=me.amount)
                e.account_changed(ar)
                entries.append(e)
        if False:  # fails in Django 1.6
            bulk_create_with_manual_ids(Entry, entries)
        else:
            for e in entries:
                e.full_clean()
                e.save()

        if self.actor_set.all().count() == 0:
            household = self.partner.get_mti_child('household')
            if household:
                mr = False
                mrs = False
                for m in household.member_set.all():
                    #~ if m.role and m.role.header:
                        #~ header = m.role.header
                    if m.person.gender == dd.Genders.male and not mr:
                        header = unicode(_("Mr."))
                        mr = True
                    elif m.person.gender == dd.Genders.female and not mrs:
                        header = unicode(_("Mrs."))
                        mrs = True
                    else:
                        header = ''
                    a = Actor(budget=self, partner=m.person, header=header)
                    a.full_clean()
                    a.save()

    @dd.virtualfield(dd.PriceField(_("Total debt")))
    def total_debt(self, ar):
        return self.sum('amount', 'L')

    @dd.htmlbox(_("Entered data"))
    def data_box(self, ar):
        # return E.div(*tuple(ar.story2html(self.data_story(ar))))
        return ar.story2html(self.data_story(ar))

    @dd.htmlbox(pgettext("debts", "Summary"))
    def summary_box(self, ar):
        # return E.div(*tuple(ar.story2html(self.summary_story(ar))))
        return ar.story2html(self.summary_story(ar))

    def data_story(self, ar):
        """Yield a sequence of """
        # logger.info("20141211 insert_story")

        def render(sar):
            if sar.renderer is None:
                raise Exception("%s has no renderer", sar)
            if sar.get_total_count():
                yield E.h3(sar.get_title())
                yield sar
            
        for eg in self.entry_groups(ar):
            yield render(eg.action_request)

    def summary_story(self, ar):

        def render(t):
            sar = ar.spawn(t, master_instance=self)
            if sar.get_total_count():
                yield E.h2(unicode(sar.get_title()))
                yield sar

        yield render(ResultByBudget)
        yield render(DebtsByBudget)
        yield render(AssetsByBudget)
        yield render(DistByBudget)


class Actor(ActorBase, SequencedBudgetComponent):
    """An **actor** of a budget is a partner who is part of the household
    for which the budget has been established.

    """
    class Meta:
        verbose_name = _("Budget Actor")
        verbose_name_plural = _("Budget Actors")

    allow_cascaded_delete = ['budget']

    partner = models.ForeignKey('contacts.Partner', blank=True)
    header = models.CharField(_("Header"), max_length=20, blank=True)
    remark = dd.RichTextField(_("Remark"), format="html", blank=True)

    def save(self, *args, **kw):
        if not self.header:
            self.header = _("Actor") + " " + str(self.seqno)
        super(Actor, self).save(*args, **kw)


class Entry(SequencedBudgetComponent):
    """A detail row of a :class:`Budget`.

    .. attribute:: budget

    The :class:`Budget` who contains this entry.

    .. attribute:: amount

        The amount of money. An empty amount is different from a zero
        amount in that the latter will be printed while the former
        not.

    .. attribute:: account

        The related :class:`Account`.

    """
    class Meta:
        verbose_name = _("Budget Entry")
        verbose_name_plural = _("Budget Entries")
        #~ unique_together = ['budget','account','name']
        #~ unique_together = ['actor','account']

    allow_cascaded_delete = ['budget']

    #~ group = models.ForeignKey(AccountGroup)
    account_type = AccountTypes.field(blank=True)
    account = models.ForeignKey('accounts.Account')
    partner = models.ForeignKey('contacts.Partner', blank=True, null=True)
    #~ name = models.CharField(_("Remark"),max_length=200,blank=True)
    #~ amount = dd.PriceField(_("Amount"),default=0)
    amount = dd.PriceField(_("Amount"), blank=True, null=True)
    actor = models.ForeignKey(Actor,
                              blank=True, null=True,
        help_text="""\
Hier optional einen Akteur angeben, wenn der Eintrag 
sich nicht auf den Gesamthaushalt bezieht.""")
    #~ amount = dd.PriceField(_("Amount"),default=0)
    circa = models.BooleanField(_("Circa"),
        default=False)
    distribute = models.BooleanField(
        _("Distribute"),
        default=False,
        help_text=u"""\
Ob diese Schuld in die Schuldenverteilung aufgenommen wird oder nicht."""
    )
    todo = models.CharField(
        verbose_name=_("To Do"), max_length=200, blank=True)
    remark = models.CharField(_("Remark"),
                              max_length=200, blank=True,
        help_text=u"Bemerkungen sind intern und werden nie ausgedruckt.")
    description = models.CharField(_("Description"),
                                   max_length=200, blank=True,
        help_text=u"""\
Beschreibung wird automatisch mit der Kontobezeichung 
ausgefüllt. Kann man aber manuell ändern. 
Wenn man das Konto ändert, gehen manuelle Änderungen in diesem Feld verloren.
Beim Ausdruck steht in Kolonne "Beschreibung"
lediglich der Inhalt dieses Feldes, der eventuellen Bemerkung sowie 
(falls angegeben bei Schulden) der Partner.""")
    periods = PeriodsField(_("Periods"),
        help_text=u"""\
Gibt an, für wieviele Monate dieser Betrag sich versteht. 
Also bei monatlichen Ausgaben steht hier 1, 
bei jährlichen Ausgaben 12.""")
    monthly_rate = dd.PriceField(_("Monthly rate"), default=0,
        help_text=u"""
Eventueller Betrag monatlicher Rückzahlungen, über deren Zahlung nicht verhandelt wird. 
Wenn hier ein Betrag steht, darf "Verteilen" nicht angekreuzt sein.
    """)

    bailiff = models.ForeignKey(
        'contacts.Company',
        verbose_name=_("Debt collection agency"),
        help_text=_("Leave empty for simple debts, otherwise select \
        here the responsible bailiff or collection agency"),
        related_name='bailiff_debts_set',
        null=True, blank=True)

    #~ duplicated_fields = """
    #~ account_type account partner actor distribute
    #~ circa todo remark description periods monthly_rate
    #~ """.split()

    def get_siblings(self):
        """
        Like super(), but adds account_type. 
        E.g. the Up/Down methods should work only within a given account_type.
        """
        #~ return super(Entry,self).get_siblings().filter(account_type=self.account_type)
        return self.__class__.objects.filter(budget=self.budget, account_type=self.account_type).order_by('seqno')

    @dd.chooser()
    def account_choices(cls, account_type):
        #~ print '20120918 account_choices', account_type
        return rt.modules.accounts.Account.objects.filter(type=account_type)

    @dd.chooser()
    def bailiff_choices(self):
        qs = rt.modules.contacts.Companies.request().data_iterator
        qs = qs.filter(client_contact_type__is_bailiff=True)
        return qs

    #~ @dd.chooser(simple_values=True)
    #~ def amount_choices(cls,account):
        #~ return [decimal.Decimal("0"),decimal.Decimal("2.34"),decimal.Decimal("12.34")]
    @dd.chooser()
    def actor_choices(cls, budget):
        return Actor.objects.filter(budget=budget).order_by('seqno')

    @dd.displayfield(_("Description"))
    def summary_description(row, ar):
        #~ chunks = [row.account]
        if row.description:
            desc = row.description
        #~ if row.partner:
            #~ chunks.append(row.partner)
            #~ return "%s/%s" join_words(unicode(row.account),unicode(row.partner),row.name)
            #~ return '/'.join([unicode(x) for x in words if x])
        #~ return join_words(unicode(row.account),row.name)
        else:
            #~ parts = [row.remark,row.partner,row.account]
            parts = [row.account, row.partner]
            desc = ' / '.join([unicode(x) for x in parts if x])
        if row.todo:
            desc += " [%s]" % row.todo
        return desc

    def account_changed(self, ar):
        if self.account_id:
            self.periods = self.account.periods
            self.description = dd.babelattr(
                self.account, 'name', language=self.budget.partner.language)

    def full_clean(self, *args, **kw):
        if self.periods <= 0:
            raise ValidationError(_("Periods must be > 0"))
        if self.distribute and self.monthly_rate:
            raise ValidationError(
                #~ _("Cannot set both 'Distribute' and 'Monthly rate'"))
                _("Cannot set 'Distribute' when 'Monthly rate' is %r") % self.monthly_rate)
        #~ self.account_type = self.account.type
        #~ if not self.account_type:
            # ~ raise ValidationError(_("Budget entry #%d has no account_type") % obj2unicode(self))
        super(Entry, self).full_clean(*args, **kw)

    def save(self, *args, **kw):
        #~ if not self.name:
            #~ if self.partner:
                #~ self.name = unicode(self.partner.name)
            #~ else:
                #~ self.name = self.account.name
        self.account_type = self.account.type
        if not self.description:
            self.description = dd.babelattr(
                self.account, 'name', language=self.budget.partner.language)
            #~ self.description = unicode(self.account)
        #~ if self.periods is None:
            #~ self.periods = self.account.periods
        super(Entry, self).save(*args, **kw)

    def on_duplicate(self, ar, master):
        """This is called when an entry has been duplicated.  It is needed
        when we are doing a "related" duplication (initiated by the
        duplication of a Budget).  In that case, `master` is not None
        but the new Budget that has been created.  We now need to
        adapt the `actor` of this Entry by making it an actor of the
        new Budget.
        
        TODO: this method relies on the fact that related Actors get
        duplicated *before* related Entries.  The order of `fklist` in
        `_lino_ddh`

        """
        if master is not None and self.actor is not None and self.actor.budget != master:
            self.actor = master.actor_set.get(seqno=self.actor.seqno)
        super(Entry, self).on_duplicate(ar, master)


dd.inject_field(
    'pcsw.ClientContactType',
    'is_bailiff',
    models.BooleanField(
        _("Debt collection agency"), default=False))

# dd.inject_field(
#     'system.SiteConfig',
#     'debts_bailiff_type',
#     models.ForeignKey("pcsw.ClientContactType",
#                       blank=True, null=True,
#                       verbose_name=_("Bailiff"),
#                       related_name='bailiff_type_sites',
#                       help_text=_("Client contact type for Bailiff.")))

dd.inject_field(
    'system.SiteConfig',
    'master_budget',
    models.ForeignKey(
        "debts.Budget",
        blank=True, null=True,
        verbose_name=_("Master budget"),
        related_name='master_budget_sites',
        help_text=_("The budget whose content is to be \
        copied into new budgets.")))

# Inject a list of fields to the accounts.Account model.
dd.inject_field('accounts.Account',
                'required_for_household',
                models.BooleanField(
                    _("Required for Households"), default=False))
dd.inject_field('accounts.Account',
                'required_for_person',
                models.BooleanField(
                    _("Required for Persons"), default=False))
dd.inject_field('accounts.Account',
                'periods',
                PeriodsField(_("Periods")))
dd.inject_field('accounts.Account',
                'default_amount',
                dd.PriceField(_("Default amount"), blank=True, null=True))

dd.inject_field('accounts.Group',
                'entries_layout',
                TableLayouts.field(_("Budget entries layout"), blank=True))


def site_setup(site):
    for T in (site.modules.contacts.Partners,
              site.modules.contacts.Persons,
              site.modules.pcsw.Clients,
              site.modules.households.Households):
        #~ T.add_detail_tab('debts.BudgetsByPartner')
        T.add_detail_tab('debts', """
        debts.BudgetsByPartner
        debts.ActorsByPartner
        """, dd.plugins.debts.verbose_name)

    #~ site.modules.accounts.Accounts.set_required(
        #~ user_groups=['debts'],user_level='manager')

    cn = "ref name default_amount periods required_for_household required_for_person group *"
    site.modules.accounts.Accounts.column_names = cn
    site.modules.accounts.AccountsByGroup.column_names = cn

    site.modules.accounts.Accounts.set_detail_layout("""
    ref name
    group type
    required_for_household required_for_person periods default_amount
    debts.EntriesByAccount
    """)

    site.modules.accounts.Groups.column_names = \
        'chart ref name account_type entries_layout *'
    site.modules.accounts.Groups.set_detail_layout("""
    ref name id
    account_type entries_layout
    AccountsByGroup
    """)

    site.modules.accounts.GroupsByChart.column_names = \
        'ref name account_type entries_layout *'


# There are no `message_extractors` for `.odt` files. One workaround
# is to manually repeat them here so that :command:`fab mm` finds
# them.

_("Financial situation")  # Finanzielle Situation
_("General information")  # Allgemeine Auskünfte
_("Name of debts mediator")  # Name des Schuldnerberaters
# _("Entered data")  # Erfasste Daten
# _("Summary")  # Zusammenfassung
# _("Conclusion")  # Schlussfolgerung

from .ui import *

AccountCharts.add_item("debts", dd.plugins.debts.verbose_name, 'debts')
