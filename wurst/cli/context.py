# encoding: utf8

from __future__ import unicode_literals

import sys

from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property

from wurst.core.consts import ISSUE_KEY_RE
from wurst.core.models import Issue, IssueType, Priority, Project, Status

from .commands import COMMANDS

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

        :param command: A string understood by shlex
        :returns: The command split into words and model instances
        :rtype: list[str|django.db.models.Model|Command]
        """
        return [self.enrich_part(part) for part in shlex.split(command)]
