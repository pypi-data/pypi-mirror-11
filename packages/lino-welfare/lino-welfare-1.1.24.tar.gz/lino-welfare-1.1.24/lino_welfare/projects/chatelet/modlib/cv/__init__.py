# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Chatelet version of CV management.  Adds Skills, Softskills and
Obstacles to :mod:`lino.modlib.cv`.  At first glanse this looks like
:mod:`lino_welfare.modlib.cv`, but it is a new implementation which
does not use the deprecated :mod:`lino.modlib.properties` plugin.

.. autosummary::
   :toctree:

   models
   fixtures.std

"""

from lino.modlib.cv import Plugin


class Plugin(Plugin):

    def setup_config_menu(self, site, profile, m):
        super(Plugin, self).setup_config_menu(site, profile, m)
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cv.SoftSkillTypes')
        m.add_action('cv.ObstacleTypes')
        m.add_action('cv.Proofs')

    def setup_explorer_menu(self, site, profile, m):
        super(Plugin, self).setup_explorer_menu(site, profile, m)
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cv.LanguageKnowledges')
        m.add_action('cv.Skills')
        m.add_action('cv.SoftSkills')
        m.add_action('cv.Obstacles')
