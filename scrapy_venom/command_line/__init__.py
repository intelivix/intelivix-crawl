# -*- coding: utf-8 -*-

import sys
from scrapy_venom.command_line import runner


__all__ = ['execute_command']


def execute_command(argv=None):
    if not argv:
        argv = sys.argv
    r = runner.ManagementRunner(argv)
    r.execute()
