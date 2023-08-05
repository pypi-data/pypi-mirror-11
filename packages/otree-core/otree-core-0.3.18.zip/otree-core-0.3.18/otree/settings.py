#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import djcelery

from django.conf import global_settings
from django.contrib.messages import constants as messages

djcelery.setup_loader()


def collapse_to_unique_list(*args):
    """Create a new list with all elements from a given lists without reapeated
    elements

    """
    combined = []
    for arg in args:
        for elem in arg or ():
            if elem not in combined:
                combined.append(elem)
    return combined


def augment_settings(settings):

    # 2015-07-10: SESSION_TYPE is deprecated
    if not 'SESSION_CONFIGS' in settings:
        settings['SESSION_CONFIGS'] = settings['SESSION_TYPES']

    if not 'SESSION_CONFIG_DEFAULTS' in settings:
        settings['SESSION_CONFIG_DEFAULTS'] = settings['SESSION_TYPE_DEFAULTS']

    all_otree_apps_set = set()
    for s in settings['SESSION_CONFIGS']:
        for app in s['app_sequence']:
            all_otree_apps_set.add(app)
    all_otree_apps = list(all_otree_apps_set)

    # order is important:
    # otree unregisters User & Group, which are installed by auth.
    # otree templates need to get loaded before the admin.
    new_installed_apps = collapse_to_unique_list(
        [
            'django.contrib.auth',
            'otree',
            'floppyforms',
            'django.contrib.admin',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'otree.models_concrete',
            'otree.timeout',
            'djcelery',
            'kombu.transport.django',
            'rest_framework',
            'sslserver',
            'idmap',
        ],


        settings['INSTALLED_APPS'],
        all_otree_apps

    )

    template_dir = os.path.join(settings['BASE_DIR'], 'templates')
    if os.path.exists(template_dir):
        additional_template_dirs = [template_dir]

    _template_dir = os.path.join(settings['BASE_DIR'], '_templates')
    if os.path.exists(_template_dir):
        additional_template_dirs = [_template_dir]

    new_template_dirs = collapse_to_unique_list(
        settings.get('TEMPLATE_DIRS'),
        # 2015-5-2: 'templates' is deprecated in favor of '_templates'
        # remove it at some point
        additional_template_dirs,
    )

    static_dir = os.path.join(settings['BASE_DIR'], 'static')
    additional_static_dirs = []
    if os.path.exists(static_dir):
        additional_static_dirs = [static_dir]

    _static_dir = os.path.join(settings['BASE_DIR'], '_static')
    if os.path.exists(_static_dir):
        additional_static_dirs = [_static_dir]

    new_staticfiles_dirs = collapse_to_unique_list(
        settings.get('STATICFILES_DIRS'),
        # 2015-5-2: 'static' is deprecated in favor of '_static'
        # remove it at some point
        additional_static_dirs,
    )

    new_middleware_classes = collapse_to_unique_list(
        [
            # this middlewware is for generate human redeable errors
            'otree.middleware.CheckDBMiddleware',
            'otree.middleware.HumanErrorMiddleware',

            'django.contrib.sessions.middleware.SessionMiddleware',
            # 'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            # 2015-04-08: disabling SSLify until we make this work better
            # 'sslify.middleware.SSLifyMiddleware',
        ],
        settings.get('MIDDLEWARE_CLASSES')
    )

    augmented_settings = {
        'INSTALLED_APPS': new_installed_apps,
        'TEMPLATE_DIRS': new_template_dirs,
        'STATICFILES_DIRS': new_staticfiles_dirs,
        'MIDDLEWARE_CLASSES': new_middleware_classes,
        'INSTALLED_OTREE_APPS': all_otree_apps,
        'BROKER_URL': 'django://',
        'MESSAGE_TAGS': {messages.ERROR: 'danger'},
        'CELERY_ACCEPT_CONTENT': ['pickle', 'json', 'msgpack', 'yaml'],
        'LOGIN_REDIRECT_URL': 'admin_home',
    }

    settings.setdefault('LANGUAGE_CODE', global_settings.LANGUAGE_CODE)

    CURRENCY_LOCALE = settings.get('CURRENCY_LOCALE', None)
    if not CURRENCY_LOCALE:

        # favor en_GB currency formatting since it represents negative amounts
        # with minus signs rather than parentheses
        if settings['LANGUAGE_CODE'][:2] == 'en':
            CURRENCY_LOCALE = 'en_GB'
        else:
            CURRENCY_LOCALE = settings['LANGUAGE_CODE']

    settings.setdefault('CURRENCY_LOCALE', CURRENCY_LOCALE.replace('-', '_'))

    logging = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'formatters': {
            'verbose': {
                'format': '[%(levelname)s|%(asctime)s] %(name)s > %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'otree.test.core': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'INFO',
            },
        }
    }

    page_footer = (
        'Powered By <a href="http://otree.org" target="_blank">oTree</a>'
    )

    overridable_settings = {

        # pages with a time limit for the player can have a grace period
        # to compensate for network latency.
        # the timer is started and stopped server-side,
        # so this grace period should account for time spent during
        # download, upload, page rendering, etc.
        'TIMEOUT_LATENCY_ALLOWANCE_SECONDS': 10,

        'SESSION_SAVE_EVERY_REQUEST': True,
        'TEMPLATE_DEBUG': settings['DEBUG'],
        'STATIC_ROOT': 'staticfiles',
        'STATIC_URL': '/static/',
        'ROOT_URLCONF': 'otree.default_urls',

        'TIME_ZONE': 'UTC',
        'USE_TZ': True,
        'SESSION_SERIALIZER': (
            'django.contrib.sessions.serializers.PickleSerializer'
        ),
        'ALLOWED_HOSTS': ['*'],

        # In pixels
        'OTREE_CHANGE_LIST_COLUMN_MIN_WIDTH': 50,

        # default to 10 seconds(10000 miliseconds)
        'OTREE_CHANGE_LIST_UPDATE_INTERVAL': '10000',
        'TEMPLATE_CONTEXT_PROCESSORS': (
            global_settings.TEMPLATE_CONTEXT_PROCESSORS +
            (
                'django.core.context_processors.request',
                'otree.context_processors.otree_context'
            )
        ),

        # SEO AND FOOTER
        'PAGE_FOOTER': page_footer,

        # list of extra string to positioning you experiments on search engines
        # Also if you want to add a particular set of SEO words to a particular
        # page add to template context "page_seo" variable.
        # See: http://en.wikipedia.org/wiki/Search_engine_optimization
        'SEO': (),

        'LOGGING': logging,

        'REAL_WORLD_CURRENCY_CODE': 'USD',
        'REAL_WORLD_CURRENCY_LOCALE': 'en_US',
        'REAL_WORLD_CURRENCY_FORMAT': None,
        'REAL_WORLD_CURRENCY_DECIMAL_PLACES': 2,

        'WSGI_APPLICATION': 'wsgi.application',
        'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
        'MTURK_HOST': 'mechanicalturk.amazonaws.com',
        'MTURK_SANDBOX_HOST': 'mechanicalturk.sandbox.amazonaws.com',
        'CREATE_DEFAULT_SUPERUSER': True,

        'CELERY_APP': 'otree.celery.app:app',

        # since workers on Amazon MTurk can return the hit
        # we need extra participants created on the
        # server.
        # The following setting is ratio:
        # num_participants_server / num_participants_mturk
        'MTURK_NUM_PARTICIPANTS_MULT': 2,
    }

    settings.update(augmented_settings)

    for k, v in overridable_settings.items():
        settings.setdefault(k, v)
