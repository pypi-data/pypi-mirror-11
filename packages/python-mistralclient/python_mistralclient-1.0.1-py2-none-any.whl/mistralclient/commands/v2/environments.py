# Copyright 2015 - StackStorm, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import argparse
import json
import logging

from cliff import command
from cliff import show
import yaml

from mistralclient.api.v2 import environments
from mistralclient.commands.v2 import base
from mistralclient import utils

LOG = logging.getLogger(__name__)


def format_list(environment=None):
    columns = (
        'Name',
        'Description',
        'Scope',
        'Created at',
        'Updated at'
    )

    if environment:
        data = (
            environment.name,
            environment.description,
            environment.scope,
            environment.created_at,
        )

        if hasattr(environment, 'updated_at'):
            data += (environment.updated_at or '<none>',)
        else:
            data += (None,)

    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


def format(environment=None):
    columns = (
        'Name',
        'Description',
        'Variables',
        'Scope',
        'Created at',
        'Updated at'
    )

    if environment:
        data = (
            environment.name,
            environment.description,
            json.dumps(environment.variables, indent=4),
            environment.scope,
            environment.created_at,
        )

        if hasattr(environment, 'updated_at'):
            data += (environment.updated_at or '<none>',)
        else:
            data += (None,)

    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


def load_file_content(f):
    content = f.read()

    try:
        data = yaml.safe_load(content)
    except:
        data = json.loads(content)

    return data


class List(base.MistralLister):
    """List all environments."""

    def _get_format_function(self):
        return format_list

    def _get_resources(self, parsed_args):
        return environments.EnvironmentManager(self.app.client).list()


class Get(show.ShowOne):
    """Show specific environment."""

    def get_parser(self, prog_name):
        parser = super(Get, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            help='Environment name'
        )

        return parser

    def take_action(self, parsed_args):
        environment = environments.EnvironmentManager(self.app.client).get(
            parsed_args.name)

        return format(environment)


class Create(show.ShowOne):
    """Create new environment."""

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)

        parser.add_argument(
            'file',
            type=argparse.FileType('r'),
            help='Environment configuration file in JSON or YAML'
        )

        return parser

    def take_action(self, parsed_args):
        data = load_file_content(parsed_args.file)
        manager = environments.EnvironmentManager(self.app.client)
        environment = manager.create(**data)

        return format(environment)


class Delete(command.Command):
    """Delete environment."""

    def get_parser(self, prog_name):
        parser = super(Delete, self).get_parser(prog_name)

        parser.add_argument('name', nargs='+', help='Name of environment(s).')

        return parser

    def take_action(self, parsed_args):
        env_mgr = environments.EnvironmentManager(self.app.client)
        utils.do_action_on_many(
            lambda s: env_mgr.delete(s),
            parsed_args.name,
            "Request to delete environment %s has been accepted.",
            "Unable to delete the specified environment(s)."
        )


class Update(show.ShowOne):
    """Update environment."""

    def get_parser(self, prog_name):
        parser = super(Update, self).get_parser(prog_name)

        parser.add_argument(
            'file',
            type=argparse.FileType('r'),
            help='Environment configuration file in JSON or YAML'
        )

        return parser

    def take_action(self, parsed_args):
        data = load_file_content(parsed_args.file)
        manager = environments.EnvironmentManager(self.app.client)
        environment = manager.update(**data)

        return format(environment)
