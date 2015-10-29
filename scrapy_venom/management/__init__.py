# -*- coding: utf-8 -*-

import sys
from .runner import ManagementRunner


__all__ = ['execute_command']


def execute_command(argv=None):
    if not argv:
        argv = sys.argv
    runner = ManagementRunner(argv)
    runner.execute()
