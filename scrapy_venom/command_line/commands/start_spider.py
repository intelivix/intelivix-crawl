# -*- coding: utf-8 -*-

import os
import sys
import shutil


def get_project_name():
    from scrapy.utils.project import get_project_settings
    settings = get_project_settings()
    project_name = settings.attributes.get('PROJECT_NAME')
    if project_name:
        return project_name.value
    return ''

project_name = get_project_name()
current_folder = os.getcwd()
project_path = os.path.join(current_folder, project_name)


pipelines_file = '''# -*- coding: utf-8 -*-
"""
    For examples, see the module "sample.pipelines"
"""

from scrapy_venom.pipelines import PipelineBase
'''

init_file = '''# -*- coding: utf-8 -*-

from .spiders import *  # noqa
'''

spider_file = '''# -*- coding: utf-8 -*-
"""
    For examples, see the module "sample.spider"
"""

from scrapy_venom.spiders import SpiderBase
'''

items_file = '''# -*- coding: utf-8 -*-
"""
    For examples, see the module "sample.items"
"""

from scrapy import Item
from scrapy import Field
'''


def path(*args):
    return os.path.join(project_path, 'spiders', *args)


def ask(message):
    yes = set(['yes', 'y', 'ye', ''])
    no = set(['no', 'n'])

    choice = raw_input(message).lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        sys.stdout.write('Por favor, responda com "s" or "n"')


def execute(*args):
    args = list(args)
    assert len(args) >= 1, u'É necessário informar pelo menos o nome da spider'

    spider_name = args.pop(0)
    spider_path = path(spider_name)

    if os.path.exists(spider_path):
        remove = ask(u'Essa spider ja existe, deseja remover? (y or n)\n')
        if remove:
            shutil.rmtree(spider_path)
        else:
            print('Cancelando acao...')
            return

    os.makedirs(spider_path)

    with open(path(spider_path, '__init__.py'), 'w+') as init:
        init.write(init_file)

    with open(path(spider_path, 'spiders.py'), 'w+') as spider:
        spider.write(spider_file)

    with open(path(spider_path, 'items.py'), 'w+') as items:
        items.write(items_file)

    with open(path(spider_path, 'pipelines.py'), 'w+') as pipelines:
        pipelines.write(pipelines_file)

    print('App criada com sucesso.')


def help():
    return u'start_spider <spider_name> - Cria uma nova spider'
