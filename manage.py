#!/usr/bin/env python

import os
import sys

from django.core import management


# Point to the correct settings for testing
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'


if __name__ == "__main__":
    testing = 'test' in sys.argv

    if testing:
        from coverage import Coverage
        cov = Coverage()
        cov.erase()
        cov.start()

    management.execute_from_command_line()

    if testing:
        cov.stop()
        cov.save()
        cov.report()
