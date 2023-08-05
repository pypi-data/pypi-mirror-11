# coding=utf-8
""" Django settings for DjangoFloor.

Settings come from 3 modules and one .ini file:

    * djangofloor.defaults
    * project-specific settings, defined in the environment variable DJANGOFLOOR_PROJECT_SETTINGS
    * user-specific settings, defined in the environment variable DJANGOFLOOR_USER_SETTINGS
    * .ini file, whose path is defined in the environment variable DJANGOFLOOR_INI_SETTINGS


djangofloor.defaults settings are overridden by project-specific settings, which are of course overridden by
    user-specific settings.

Only variables in uppercase (like INSTALLED_APPS) are taken into account.
Only variables defined in djangofloor.defaults or in project-specific settings are taken into account.

If VARIABLE is uppercase and if VARIABLE_HELP exists, then VARIABLE is shown with command `manage.py config`.

"""
from __future__ import unicode_literals, print_function
from django.utils.module_loading import import_string

try:
    # noinspection PyCompatibility
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences,PyCompatibility
    from ConfigParser import ConfigParser

from django.utils import six
from django.utils.encoding import force_text

import os
import string
import sys
# noinspection PyCompatibility
from pathlib import Path
from djangofloor import defaults as floor_settings
from djangofloor.utils import DirectoryPath, FilePath, import_module

__author__ = 'Matthieu Gallet'

PROJECT_SETTINGS_MODULE_NAME = os.environ.get('DJANGOFLOOR_PROJECT_DEFAULTS', '')
USER_SETTINGS_PATH = os.environ.get('DJANGOFLOOR_PYTHON_SETTINGS', '')
DJANGOFLOOR_CONFIG_PATH = os.environ.get('DJANGOFLOOR_INI_SETTINGS', '')
DJANGOFLOOR_MAPPING = os.environ.get('DJANGOFLOOR_MAPPING', '')
PROJECT_NAME = os.environ.get('DJANGOFLOOR_PROJECT_NAME', 'djangofloor')


def import_file(filepath):
    """import the Python source file as a Python module.

    :param filepath: absolute path of the Python module
    :type filepath: :class:`str`
    :return:
    """
    if filepath and os.path.isfile(filepath):
        dirname = os.path.dirname(filepath)
        if dirname not in sys.path:
            sys.path.insert(0, dirname)
        conf_module = os.path.splitext(os.path.basename(filepath))[0]
        module_ = import_module(conf_module)
    elif filepath:
        import djangofloor.empty
        module_ = djangofloor.empty
    else:
        import djangofloor.empty
        module_ = djangofloor.empty
    return module_

# default settings for the project
if PROJECT_SETTINGS_MODULE_NAME:
    project_settings = import_module(PROJECT_SETTINGS_MODULE_NAME)
else:
    import djangofloor.empty
    project_settings = djangofloor.empty

# settings for the installation
user_settings = import_file(USER_SETTINGS_PATH)

# load settings from the .ini configuration file
ini_config_mapping = {}
if DJANGOFLOOR_MAPPING:
    try:
        ini_values = import_string(DJANGOFLOOR_MAPPING)
        if os.path.isfile(DJANGOFLOOR_CONFIG_PATH):
            parser = ConfigParser()
            parser.read([DJANGOFLOOR_CONFIG_PATH])
            for option_parser in ini_values:
                option_parser(parser, ini_config_mapping)
    except ImportError:
        pass


__settings = globals()
__formatter = string.Formatter()
__settings_origin = {}


def __parse_setting(obj):
    """Parse the object for replacing variables by their values.
    If `obj` is a string like "THIS_IS_{TEXT}", search for a setting named "TEXT" and replace {TEXT} by its value (say, "VALUE").
    The returned object is then equal to "THIS_IS_VALUE".
    If `obj` is a list, a set, a tuple or a dict, their components are recursively parsed.
    If `obj` is a DirectoryPath or a FilePath, required parent directories are automatically created and the name is returned.
    Otherwise, `obj` is returned as-is.


    :param obj: object to analyze
    :return: the parsed setting
    """
    if isinstance(obj, six.text_type):
        values = {'PROJECT_NAME': PROJECT_NAME}
        for (literal_text, field_name, format_spec, conversion) in __formatter.parse(obj):
            if field_name is not None:
                values[field_name] = __setting_value(field_name)
        if values:
            return __formatter.format(obj, **values)
    elif isinstance(obj, DirectoryPath):
        obj = __parse_setting(force_text(obj))
        __ensure_dir(obj, parent_=False)
        return obj
    elif isinstance(obj, FilePath):
        obj = __parse_setting(force_text(obj))
        __ensure_dir(obj, parent_=True)
        return obj
    elif isinstance(obj, Path):
        return __parse_setting(force_text(obj))
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [__parse_setting(x_) for x_ in obj]
    elif isinstance(obj, set):
        return {__parse_setting(x_) for x_ in obj}
    elif isinstance(obj, dict):
        return dict([(__parse_setting(x_), __parse_setting(y_)) for (x_, y_) in obj.items()])
    return obj


def __setting_value(setting_name_):
    """ import setting_name_ from user-specific settings, or project-specific settings, or django-floor settings.
    Also add it to globals(), so this function is idempotent.

    :param setting_name_: name of the setting to import
    :return: the imported setting :)
    """
    if setting_name_ in __settings:
        return __settings[setting_name_]
    if hasattr(user_settings, setting_name_):
        value = getattr(user_settings, setting_name_)
        __settings_origin[setting_name_] = USER_SETTINGS_PATH
    elif setting_name_ in ini_config_mapping:
        value = ini_config_mapping[setting_name_]
        __settings_origin[setting_name_] = DJANGOFLOOR_CONFIG_PATH
    elif hasattr(project_settings, setting_name_):
        value = getattr(project_settings, setting_name_)
        __settings_origin[setting_name_] = 'project\'s defaults'
    else:
        value = getattr(floor_settings, setting_name_)
        __settings_origin[setting_name_] = 'djangofloor\'s defaults'
    __settings[setting_name_] = __parse_setting(value)
    return __settings[setting_name_]


def __ensure_dir(path_, parent_=True):
    """ ensure that the given directory exists
    :param path_: the path to check
    :param parent_: only ensure the existence of the parent directory
    """
    dirname_ = os.path.dirname(path_) if parent_ else path_
    if not os.path.isdir(dirname_):
        try:
            os.makedirs(dirname_)
            print('Directory %s created.' % dirname_)
        except IOError:
            print('Unable to create directory %s.' % dirname_)


for module in floor_settings, project_settings, user_settings:
    for setting_name in module.__dict__:
        if setting_name == setting_name.upper():
            __setting_value(setting_name)

# add extra installed app
# noinspection PyUnresolvedReferences
for y in OTHER_ALLAUTH, FLOOR_INSTALLED_APPS:
    for x in y:
        # noinspection PyUnresolvedReferences
        if x and x not in INSTALLED_APPS:
            # noinspection PyUnresolvedReferences
            INSTALLED_APPS.append(x)

if __name__ == '__main__':
    import doctest

    doctest.testmod()
