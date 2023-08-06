"""
Interface for sous chefs.
"""
import types
from traceback import format_exc
from collections import defaultdict

from newslynx.client import API
from newslynx.exc import (
    SousChefInitError, SousChefExecError)
from newslynx.logs import StdLog, ColorLog


class SousChef(object):

    """
    A SousChef gets an org, a user's apikey, and a recipe
    and modifies NewsLynx via it's API.
    """

    timeout = 120  # how long until this sous chef timesout?

    def __init__(self, **kw):

        # parse required kwargs
        self.org = kw.pop('org')
        self.apikey = kw.pop('apikey')
        self.recipe = kw.pop('recipe', {})
        self.config = kw.pop('config', {})
        if not self.org or not self.recipe or not self.apikey or not self.config:
            raise SousChefInitError(
                'A SousChef requires a "org", "recipe", and "apikey" to run.')

        self.passthrough = kw.pop('passthrough', False)
        self.log = ColorLog(**kw)  # TODO: logging configuration.

        # api connection
        self.api = API(apikey=self.apikey, org=self.org['id'])

        # full org object
        self.auths = self.org.pop('auths', {})
        self.settings = self.org.pop('settings', {})
        self.users = self.org.pop('users', [])

        # options for this recipe
        # allow arbitrary runtime arguments.
        self.options = self.recipe.get('options', **kw)
        self.recipe_id = self.recipe.get('id', None)

        # handle cache-clears between jobs.
        self.next_job = defaultdict(dict)

        if not self.passthrough:
            lj = self.recipe.get('last_job', None)
            if lj is None:
                self.last_job = defaultdict(dict)
            elif not isinstance(lj, dict):
                self.last_job = defaultdict(dict)
            else:
                self.last_job = lj

        # passthrough jobs should not use contextual
        # variables.
        else:
            self.last_job = defaultdict(dict)

    def setup(self):
        return True

    def run(self):
        raise NotImplemented('A SousChef requires a `run` method.')

    def serialize(self, data):
        """
        Validate and serialize run output.
        """
        if isinstance(data, (types.ListType, types.GeneratorType)):
            for item in data:
                # allow for to-dict protocol
                if hasattr(item, 'to_dict'):
                    item = item.to_dict()

                elif isinstance(item, (types.DictType)):
                    yield item

        elif isinstance(data, (types.DictType)):
            yield data

        elif hasattr(data, 'to_dict'):
            yield data.to_dict()

        else:
            raise SousChefExecError(
                "Invalid output type: {}\n"
                "run should return either a dictionary or "
                "a list or generator or single dictionaries or "
                "object with a .to_dict() method".format(type(data))
            )

    def load(self, data):
        return data

    def teardown(self):
        return True

    def cook(self):
        """
        The SousChef's workflow.
        """
        # always setup run and serialize.
        try:
            self.setup()
            data = self.run()
            if not data:
                return
            data = self.serialize(data)

            # passthrough jobs should not 'load'
            if not self.passthrough:
                data = self.load(data)  # load the data.
            return data

        except Exception:
            raise SousChefExecError(format_exc())
