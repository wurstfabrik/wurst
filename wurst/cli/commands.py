# encoding: utf-8

from __future__ import unicode_literals

from django.core.exceptions import ValidationError

from wurst.core.models import Issue


class Command(object):
    slug = None
    verbs = set()

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Not implemented.")


class CreateCommand(Command):
    slug = "create"
    verbs = {"create", "new", "c"}

    def execute(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        issue_type = kwargs.pop("issuetype", None)
        title = " ".join(args)
        if not title:
            raise ValidationError("Issue title is required.")
        if not project:
            raise ValidationError("A project is required.")
        if not issue_type:
            raise ValidationError("An issue type is required.")

        return Issue.objects.create(project=project, type=issue_type, title=title)


class SetCommand(Command):
    slug = "set"
    verbs = {"set", "s"}


COMMANDS = [CreateCommand, SetCommand]
