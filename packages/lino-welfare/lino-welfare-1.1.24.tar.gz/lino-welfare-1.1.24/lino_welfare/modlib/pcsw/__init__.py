# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)


"""

The :mod:`lino_welfare.modlib.pcsw` package provides data definitions
for PCSW specific objects.

Most important models are :class:`Client` and :class:`Coaching`.

.. autosummary::
   :toctree:

    roles
    mixins
    choicelists
    models
    coaching
    fixtures
    utils

See also :mod:`welfare.pcsw`.

"""


from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("PCSW")

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('pcsw.CoachedClients')
        m.add_action('pcsw.MyCoachings')

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('pcsw.PersonGroups')
        m.add_action('pcsw.Activities')
        m.add_action('pcsw.ExclusionTypes')
        m.add_action('pcsw.CoachingTypes')
        m.add_action('pcsw.CoachingEndings')
        m.add_action('pcsw.DispenseReasons')
        m.add_action('pcsw.ClientContactTypes')
        if not site.is_installed('aids'):
            m.add_action('pcsw.AidTypes')

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('pcsw.Coachings')
        m.add_action('pcsw.ClientContacts')
        m.add_action('pcsw.Exclusions')
        m.add_action('pcsw.Convictions')
        m.add_action('pcsw.AllClients')
        #~ m.add_action(PersonSearches)
        m.add_action('pcsw.CivilState')
        m.add_action('pcsw.ClientStates')
        m.add_action('beid.BeIdCardTypes')

