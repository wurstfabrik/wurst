# encoding: utf8

from __future__ import unicode_literals

import sys
from inspect import isclass

import six
from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property

from wurst.core.consts import ISSUE_KEY_RE
from wurst.core.models import Issue, IssueType, Priority, Project, Status
from wurst.core.models.workflow import Transition

from .commands import BaseTransitionCommand, COMMANDS

if sys.version_info[0] < 3:
    import ushlex as shlex
else:
    import shlex

NOUN_CLASSES = [IssueType, Status, Priority, Project]


class Context(object):
    """
    A Context contains the hot words for the current environment (project etc.) mapped to their
    model counterparts.
    """

    @cached_property
    def terms(self):
        """
        A cached dictionary of known nouns and verbs.
        """

        the_terms = dict()

        for NounClass in NOUN_CLASSES:
            for item in NounClass.objects.all():
                for noun in item.get_nouns():
                    assert noun not in the_terms

                    the_terms[noun] = item

        for command in COMMANDS:
            for verb in command.verbs:
                assert verb not in the_terms

                the_terms[verb] = command

        for transition in Transition.objects.all():
            command_class = type(
                # NB: The use of `str` here is perfectly on purpose:
                #     on Python 2, class names must be ASCII strings,
                #     and Python 3 doesn't mind at all.
                str("%sTransitionCommand" % transition.slug.title()),
                (BaseTransitionCommand,),
                {"transition": transition}
            )
            for verb in transition.get_verbs():
                the_terms[verb] = command_class

        return the_terms

    def enrich_part(self, part):
        """
        Enriches a single part (which, well, might contain more than one actual word).

        :param part: A part(-of-speech) to enrich.
        :return: The part itself, or a model.
        """

        if part in self.terms:  # Try the "static" part dictionary...
            return self.terms[part]

        if ISSUE_KEY_RE.match(part):  # See if the part smells like an issue key...
            try:
                return Issue.objects.get(key=part)
            except ObjectDoesNotExist:
                pass

        # See if it's an unique prefix (if it's long enough anyway)
        if len(part) > 2:
            prefix_matches = [obj for (term, obj) in self.terms.items() if term.startswith(part)]
            if len(prefix_matches) == 1:
                return prefix_matches[0]

        return part

    def enrich_command(self, command):
        """
        Enriches the command by replacing recognized words with their model instance counterparts.

        If multiple terms referring to known classes are found, only one is enriched; the rest are not
        enriched but returned as-is.

        :param command: A string understood by shlex
        :returns: The command split into words and model instances
        :rtype: Iterable[str|django.db.models.Model|Command]
        """
        found_classes = set()
        for part in shlex.split(command):
            e_part = self.enrich_part(part)
            if not isinstance(e_part, six.string_types):
                if isclass(e_part):
                    cls = e_part
                else:
                    cls = e_part.__class__
                if cls not in found_classes:
                    found_classes.add(cls)
                else:
                    e_part = part  # Revert back to yielding the string
            yield e_part
