import os
import re
import importlib

from jsonschema import Draft4Validator

from newslynx.sc import SousChef as SC
from newslynx.exc import SousChefSchemaError
from newslynx.models import SousChef
from newslynx.lib.serialize import yaml_to_obj
from newslynx.lib.serialize import obj_to_json, json_to_obj
from newslynx.constants import SOUS_CHEF_RESERVED_FIELDS
from newslynx.util import here, update_nested_dict

# load souschef schema + validator.
SOUS_CHEF_JSON_SCHEMA = yaml_to_obj(
    open(here(__file__, 'sous_chef.yaml')).read())

# these are default options that all sous chefs have.
SOUS_CHEF_DEFAULT_OPTIONS = yaml_to_obj(
    open(here(__file__, 'sous_chef_default_options.yaml')).read())

# a json-schema validator for a sous chef.
SOUS_CHEF_VALIDATOR = Draft4Validator(SOUS_CHEF_JSON_SCHEMA)

# a regex for validation option + metric names
re_opt_name = re.compile(r'^[a-z][a-z_]+[a-z]$')


def validate(sc):
    """
    Validate a sous chef schema:
    First chef against the canoncial json schema.
    Then check if the `runs` field is a valid python
    module or an executable script that exists where
    it has been declared. Then check special metrics
    options and merge the default sous-chef options
    with the provied ones.
    """

    # check the json schema
    _validate_sous_chef_json_schema(sc)

    # check for checkbox option sous chefs
    _validate_input_and_value_types(sc)

    # check if `runs` is a python module that inherits from
    # newslynx.sc.SousChef
    if not '/' in sc['runs']:
        sc['is_command'] = False
        _validate_python_sous_chef(sc)

    # otherwise validate the command
    else:
        sc['is_command'] = True
        _validate_command_sous_chef(sc)

    # special cases for sous chefs that create metrics
    if sc['creates'] == 'metrics':
        _validate_metrics_sous_chef(sc)

    # if everything is kosher, merge the sous-chef options
    # with the defaults
    sc['options'] = update_nested_dict(
        sc['options'], SOUS_CHEF_DEFAULT_OPTIONS)
    return sc


def update(old_sous_chef, new_sous_chef):
    """
    Given a partial or completely new sous-chef, update the souf-chef
    and re-validate it.
    """

    # if the old sous chef is a SousChef object, coerce it to and from json.
    if isinstance(old_sous_chef, SousChef):
        old_sous_chef = json_to_obj(obj_to_json(old_sous_chef))

    # pop the id
    old_sous_chef.pop('id', None)

    # update the previous version.
    new_sous_chef = update_nested_dict(
        old_sous_chef, new_sous_chef, overwrite=True)

    return validate(new_sous_chef)


def _validate_input_and_value_types(sc):
    """
    Special cases for sous chefs that have checkbox option.
    """
    slug = sc.get('slug')
    opts = sc.get('options', {})
    for k, v in opts.items():

        if not re_opt_name.match(k):
            raise SousChefSchemaError(
                "Error validating: '{}' - Option '{}' for SousChef '{}' is invalid. "
                "Options must follow the naming convention of '{}'."
                .format(slug, re_opt_name.pattern))

        if k in SOUS_CHEF_RESERVED_FIELDS:
                msg = "Invalid option '{}' - '{}' Is a reserved option name."\
                      .format(k, k)
                _raise_sous_chef_schema_error(sc, msg)

        elif v.get('input_type') == 'checkbox' and \
                not v.get('accepts_list', False):
                msg = "Invalid option '{}' - Options with a 'checkbox' input_type must "\
                      "accept multiple inputs."\
                      .format(k)
                _raise_sous_chef_schema_error(sc, msg)

        elif v.get('input_type') == 'datepicker' and \
                not 'datetime' in v.get('value_types'):
                msg = "Invalid option '{}' - Options with a 'datepicker' input_type must "\
                      "include 'datetime' in value_types."\
                      .format(k)
                _raise_sous_chef_schema_error(sc, msg)

        elif v.get('input_type') == 'number' and \
                not 'numeric' in v.get('value_types'):
                msg = "Invalid option '{}' - Options with a 'number' input_type must "\
                      "include 'numeric' in value_types."\
                      .format(k)
                _raise_sous_chef_schema_error(sc, msg)

        elif 'searchstring' in v.get('value_types') and \
                not v.get('input_type') == 'text':
                msg = "Invalid option '{}' -  Options with a value_type of 'searchstring' "\
                      "must have an input_type of 'text'."\
                      .format(k)
                _raise_sous_chef_schema_error(sc, msg)

        elif 'url' in v.get('value_types') and \
                not v.get('input_type') == 'text':
                msg = "Invalid option '{}' -  Options with a value_type of 'url'"\
                      "must have an input_type of 'text'."\
                      .format(k)
                _raise_sous_chef_schema_error(sc, msg)

        elif 'email' in v.get('value_types') and \
                not v.get('input_type') == 'text':
                msg = "Invalid option '{}' - Options with a value_type of 'email' "\
                      "must have an input_type of 'text'."\
                      .format(k)
                _raise_sous_chef_schema_error(sc, msg)

        elif 'regex' in v.get('value_types') and \
                not v.get('input_type') == 'text':
                msg = "Invalid option '{}' - Options with a value_type of 'regex' "\
                      "must have an input_type of 'text'."\
                      .format(k)
                _raise_sous_chef_schema_error(sc, msg)


def _validate_metrics_sous_chef(sc):
    """
    Special cases for sous chefs that create metrics.
    """
    metrics = sc.get('metrics', {})
    if not len(metrics.keys()):
        msg = 'SousChefs that create metrics must explicitly declare the metrics they create.'
        _raise_sous_chef_schema_error(sc, msg)

    # check special metrics edge cases.
    for name, config in metrics.items():

        if not re_opt_name.match(name):
            msg = "metric '{}' is invalid. Metrics must follow the naming convention of '{}'."\
                  .format(re_opt_name.pattern)
            _raise_sous_chef_schema_error(sc, msg)

        # TODO MORE checking logic.


def _validate_sous_chef_json_schema(sc):
    """
    Check if a sous chef follows the core JSON schema.
    """
    # call this error here so we can raise more informative errors
    # down the line.
    if not sc.get('slug', None):
        raise SousChefSchemaError('A SousChef must have a slug!')
    schema_errors = sorted(
        SOUS_CHEF_VALIDATOR.iter_errors(sc), key=lambda e: e.path)

    if len(schema_errors):
        msg = "This config does not match the json schema. Here are the errors:"
        for error in schema_errors:
            path = ".".join([str(i) for i in error.path])
            msg += "\n{} - {}".format(path, error.message)
        _raise_sous_chef_schema_error(sc, msg)


def _validate_python_sous_chef(sc):
    """
    Check if a python SousChef is valid.
    """
    try:

        import_parts = sc['runs'].split('.')
        module = '.'.join(import_parts[:-1])
        c = import_parts[-1]
        m = importlib.import_module(module)
        sous_chef = getattr(m, c, None)

        if not sous_chef:
            msg = '{} does not exist in module {}.'.format(c, module)
            _raise_sous_chef_schema_error(sc, msg)

    except ImportError:
        msg = "{} is not importable.".format(module)
        _raise_sous_chef_schema_error(sc, msg)

    if not issubclass(sous_chef, SC):
        msg = "{} does not inherit from newslynx.sc.SousChef.".format(
            sc['runs'])
        _raise_sous_chef_schema_error(sc, msg)


def _validate_command_sous_chef(sc):
    """
    Check if an executable SousChef is valid.
    """
    if not sc['runs'].startswith('/'):
        msg = '{} does not have an absolute path.'.format(sc['runs'])
        _raise_sous_chef_schema_error(sc, msg)

    if not os.path.exists(sc['runs']):
        msg = '{} does not exist.'.format(sc['runs'])
        _raise_sous_chef_schema_error(sc, msg)

    if not os.access(sc['runs'], os.X_OK):
        msg = '{} is not an executable.'.format(sc['runs'])
        _raise_sous_chef_schema_error(sc, msg)


def _raise_sous_chef_schema_error(sc, message):
    """
    A helper for raising consistent error messages.
    """
    preface = "There were problems validating SousChef '{slug}': ".format(**sc)
    msg = preface + message
    raise SousChefSchemaError(msg)
