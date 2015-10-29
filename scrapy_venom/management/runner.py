# -*- coding: utf-8 -*-

from importlib import import_module
from . import commands


__all__ = ['ManagementRunner']


def get_custom_commands_path():
    from scrapy.utils.project import get_project_settings
    settings = get_project_settings()
    return settings.attributes.get('MANAGE_COMMANDS_PATH').value


class ManagementRunner(object):

    def __init__(self, argv=None):
        self.argv = argv or []

    def get_custom_commands(self):
        return import_module(get_custom_commands_path())

    def execute(self):
        try:
            self.argv.pop(0)
            command = self.argv.pop(0)
        except IndexError:
            command = 'help'

        if hasattr(commands, command):
            command = getattr(commands, command)
            command.execute(*self.argv)

        else:
            custom_commands = self.get_custom_commands()
            if hasattr(custom_commands, command):
                command = getattr(custom_commands, command)
                command.execute(*self.argv)
            else:
                commands.help.execute()
