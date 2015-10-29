# -*- coding: utf-8 -*-

from .utils import get_project_name


__all__ = ['register_spiders']


def generate_path(project_name, spider_name):
    return '{}.spiders.{}'.format(project_name, spider_name)


def register_spiders(*args):
    project_name = get_project_name()
    spider_modules = []
    for spider_name in args:
        module_path = generate_path(project_name, spider_name)
        spider_modules.append(module_path)
    return spider_modules
