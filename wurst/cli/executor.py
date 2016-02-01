# -- encoding: UTF-8 --
from inspect import isclass

import six
from django.db.models import Model

from wurst.cli.commands import Command
from wurst.cli.context import Context


def execute(command, context=None):
    """
    Execute a CLI command; return the return value.

    :param command: A command string or list of enriched parts.
    :return: Anything! Really!
    """

    if isinstance(command, six.string_types):
        if not context:
            context = Context()
        parts = list(context.enrich_command(command))
    else:
        parts = list(command)

    cmd_class, args, kwargs = prepare_parts(parts)

    return cmd_class().execute(*args, **kwargs)


def prepare_parts(parts):
    kwargs = {}
    args = []
    cmd_class = None
    for part in parts:
        if isinstance(part, Model):
            kwargs[part._meta.model_name] = part
        elif isclass(part) and issubclass(part, Command):
            cmd_class = part
        else:
            args.append(part)
    # TODO: This would be a good spot for turning more args into kwargs!
    return (cmd_class, args, kwargs)
