# encoding: utf-8

from __future__ import unicode_literals

from collections import namedtuple

# Stub, replace with a real Command class
Command = namedtuple("Command", "slug verbs")

wurst = Command(slug="wurst", verbs=["wurst"])  # mostly ignored
create = Command(slug="create", verbs=["create", "new", "c"])

COMMANDS = [wurst, create]
