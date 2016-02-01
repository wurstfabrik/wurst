# encoding: utf8

from __future__ import unicode_literals

import sys

from django.utils.functional import cached_property

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

    def enrich_command(self, command):
        """
        Enriches the command by replacing recognized words with their model instance counterparts.

        :param command: A string understood by shlex
        :returns: The command split into words and model instances
        :rtype: list[str|django.db.models.Model|Command]
        """
        return [self.terms.get(part, part) for part in shlex.split(command)]
