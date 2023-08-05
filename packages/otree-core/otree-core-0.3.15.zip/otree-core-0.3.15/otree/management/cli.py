import os
import platform
import subprocess
import sys

import django
import django.core.management
from django.core.management.base import CommandError
from django.core.management.color import color_style
from django.conf import settings

import otree


# =============================================================================
# CONSTANTS
# =============================================================================

MANAGE_URL = (
    "https://raw.githubusercontent.com/oTree-org/oTree/master/manage.py"
)


# =============================================================================
# FUNCTIONS
# =============================================================================

def otree_get_version(*args, **kwargs):
    """this function patch the original get version of django"""
    otree_ver = otree.get_version()
    django_ver = django.get_version()
    return "oTree: {} - Django: {}".format(otree_ver, django_ver)


def execute_from_command_line(arguments, script_file):
    # Workaround for windows. Celery (more precicely the billard library) will
    # complain if the script you are using to initialize celery does not end
    # on '.py'. That's why we require a manage.py file to be around.
    # See https://github.com/celery/billiard/issues/129 for more details.

    cond = (
        platform.system() == 'Windows' and not
        script_file.lower().endswith('.py')
    )

    if cond:

        scriptdir = os.path.dirname(os.path.abspath(script_file))
        managepy = os.path.join(scriptdir, 'manage.py')
        if not os.path.exists(managepy):
            error_lines = []

            error_lines.append(
                "It seems that you do not have a file called 'manage.py' in "
                "your current directory. This is a requirement when using "
                "otree on windows."
            )
            error_lines.append("")
            error_lines.append("")
            error_lines.append(
                "Please download the file {url} and save it as 'manage.py' in "
                "the directory {directory}".format(
                    url=MANAGE_URL, directory=scriptdir
                )
            )
            raise CommandError("\n".join(error_lines))
        args = [sys.executable] + [managepy] + sys.argv[1:]
        process = subprocess.Popen(args,
                                   stdin=sys.stdin,
                                   stdout=sys.stdout,
                                   stderr=sys.stderr)
        return_code = process.wait()
        sys.exit(return_code)

    # in issue #300 we agreed that sslserver should
    # run only if user has specified credentials for AWS
    if (len(sys.argv) >= 2 and sys.argv[1] == 'runserver' and
       settings.AWS_ACCESS_KEY_ID):
            sys.argv[1] = 'runsslserver'

    # only monkey path when is necesary
    if "version" in arguments or "--version" in arguments:
        django.core.management.get_version = otree_get_version

    django.core.management.execute_from_command_line(sys.argv)


def main():
    """
    This function is the entry point for the ``otree`` console script.
    """

    # We need to add the current directory to the python path as this is not
    # set by default when no using "python <script>" but a standalone script
    # like ``otree``.
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    style = color_style()

    try:
        from django.conf import settings
        settings.INSTALLED_APPS
    except ImportError:
        print(style.ERROR(
            "Cannot import otree settings. Please make sure that you are "
            "in the base directory of your oTree library checkout. "
            "This directory contains a settings.py and a manage.py file."))
        sys.exit(1)

    execute_from_command_line(sys.argv, 'otree')
