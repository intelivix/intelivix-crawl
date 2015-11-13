# -*- coding: utf-8 -*-

import glob
import os
from importlib import import_module


def get_project_path():
    from scrapy.utils.project import get_project_settings
    settings = get_project_settings()
    project = settings.attributes.get('PROJECT_NAME')
    project_name = ''
    if project:
        project_name = project.value

    current_folder = os.getcwd()
    return os.path.join(current_folder, project_name)


def print_commands():
    path = os.path.dirname(os.path.abspath(__file__))
    regex_path = os.path.join(path, '*.py')

    for file_name in sorted(glob.glob(regex_path)):
        command = os.path.basename(file_name.replace('.py', ''))
        if not command.startswith('_'):
            module = import_module('scrapy_venom.management.commands.{}'.format(command))
            if hasattr(module, 'help'):
                print('   => {}'.format(module.help()))
            else:
                print('   => {}'.format(command))


def get_custom_commands():
    project_path = get_project_path()
    custom_commands_path = os.path.join(project_path, 'commands')
    if os.path.exists(custom_commands_path):
        regex_path = os.path.join(custom_commands_path, '*.py')
        for file_name in sorted(glob.glob(regex_path)):
            command = os.path.basename(file_name.replace('.py', ''))
            if not command.startswith('_'):
                yield command


def header(text):
    print('\033[95m{}\033[94m'.format(text))


def br():
    print('\n')


def execute(*args):
    br()
    header('=========================')
    header('Scrapy-venom commands')
    header('=========================')

    print_commands()

    br()
    header('=========================')
    header('Custom commands available')
    header('=========================')

    for custom in get_custom_commands():
        print('   => {}'.format(custom))

    br()
