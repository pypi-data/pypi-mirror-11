# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.modlib.courses.models import *

CourseAreas.clear()
add = CourseAreas.add_item
add('S', _("Integration workshops"), 'integ')  # no longer used
add('B', _("Basic skills"), 'basic')
add('J', _("Job search modules"), 'job')

add = EnrolmentStates.add_item
add('40', _("Started"), 'started', invoiceable=False, uses_a_place=True)
add('50', _("Finished"), 'finished', invoiceable=False, uses_a_place=False)


@dd.receiver(dd.pre_analyze)
def my_enrolment_workflows(sender=None, **kw):

    EnrolmentStates.started.add_transition(
        required_states="confirmed requested")
    EnrolmentStates.finished.add_transition(
        required_states="started")


class Course(Course):
    class Meta:
        verbose_name = _("Workshop")
        verbose_name_plural = _('Workshops')
        abstract = dd.is_abstract_model(__name__, 'Course')


class Enrolment(Enrolment):
    """Adds two text fields :attr:`motivation` and :attr:`problems`.

    """
    motivation = dd.RichTextField(
        _("Motif de l'orientation"),
        blank=True, format="html")
    problems = dd.RichTextField(
        _("Difficultés à l'origine de la demande / "
          "Problématiques repérées"),
        blank=True, format="html")

Enrolments.detail_layout = """
request_date user
course pupil
remark amount workflow_buttons printed
motivation problems
"""


class Line(Line):
    class Meta:
        verbose_name = _("Workshop series")
        verbose_name_plural = _('Workshop lines')
        abstract = dd.is_abstract_model(__name__, 'Line')


EnrolmentsByPupil.column_names = 'request_date course workflow_buttons *'


class IntegEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.integ


class BasicEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.basic


class JobEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.job


