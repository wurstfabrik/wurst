# encoding: utf-8

from __future__ import unicode_literals


class Command(object):
    slug = None
    verbs = set()


class CreateCommand(Command):
    slug = "create"
    verbs = {"create", "new", "c"}


class SetCommand(Command):
    slug = "set"
    verbs = {"set", "s"}


COMMANDS = [CreateCommand, SetCommand]
