# Copyright 2014 - Mirantis, Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import json
import logging

from cliff import command
from cliff import show

from mistralclient.api.v2 import action_executions
from mistralclient.commands.v2 import base

LOG = logging.getLogger(__name__)


def format_list(action_ex=None):
    return format(action_ex, lister=True)


def format(action_ex=None, lister=False):
    columns = (
        'ID',
        'Name',
        'Workflow name',
        'Task name',
        'State',
        'State info',
        'Is accepted',
    )

    if action_ex:
        state_info = (action_ex.state_info if not lister
                      else base.cut(action_ex.state_info))

        data = (
            action_ex.id,
            action_ex.name,
            action_ex.workflow_name,
            action_ex.task_name if hasattr(action_ex, 'task_name') else None,
            action_ex.state,
            state_info,
            action_ex.accepted,
        )
    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


class Create(show.ShowOne):
    """Create new Action execution or just run specific action."""

    def produce_output(self, parsed_args, column_names, data):
        if not column_names:
            return 0

        return super(Create, self).produce_output(
            parsed_args,
            column_names,
            data
        )

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            help='Action name to execute.'
        )
        parser.add_argument(
            dest='input',
            nargs='?',
            help='Action input.'
        )
        parser.add_argument(
            '-s',
            '--save-result',
            dest='save_result',
            action='store_true',
            help='Save the result into DB.'
        )
        parser.add_argument(
            '-t',
            '--target',
            dest='target',
            help='Action will be executed on <target> executor.'
        )

        return parser

    def take_action(self, parsed_args):
        params = {}

        if parsed_args.save_result:
            params['save_result'] = parsed_args.save_result

        if parsed_args.target:
            params['target'] = parsed_args.target

        action_input = None

        if parsed_args.input:
            try:
                action_input = json.loads(parsed_args.input)
            except:
                action_input = json.load(open(parsed_args.input))

        action_ex = action_executions.ActionExecutionManager(
            self.app.client
        ).create(
            parsed_args.name,
            action_input,
            **params
        )

        if parsed_args.save_result:
            return format(action_ex)
        else:
            self.app.stdout.write("%s\n" % action_ex.output)

            return None, None


class List(base.MistralLister):
    """List all Action executions."""

    def _get_format_function(self):
        return format_list

    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)

        parser.add_argument(
            'task_execution_id',
            nargs='?',
            help='Task execution ID.')

        return parser

    def _get_resources(self, parsed_args):
        return action_executions.ActionExecutionManager(
            self.app.client
        ).list(parsed_args.task_execution_id)


class Get(show.ShowOne):
    """Show specific Action execution."""

    def get_parser(self, prog_name):
        parser = super(Get, self).get_parser(prog_name)

        parser.add_argument(
            'id',
            help='Action execution ID.')
        return parser

    def take_action(self, parsed_args):
        execution = action_executions.ActionExecutionManager(
            self.app.client
        ).get(parsed_args.id)

        return format(execution)


class Update(show.ShowOne):
    """Update specific Action execution."""

    def get_parser(self, prog_name):
        parser = super(Update, self).get_parser(prog_name)

        parser.add_argument(
            'id',
            help='Action execution ID.')
        parser.add_argument(
            '--state',
            dest='state',
            choices=['IDLE', 'RUNNING', 'SUCCESS', 'ERROR'],
            help='Action execution state')
        parser.add_argument(
            '--output',
            dest='output',
            help='Action execution output')

        return parser

    def take_action(self, parsed_args):
        output = None
        if parsed_args.output:
            try:
                output = json.loads(parsed_args.output)
            except:
                output = json.load(open(parsed_args.output))

        execution = action_executions.ActionExecutionManager(
            self.app.client
        ).update(
            parsed_args.id,
            parsed_args.state,
            output
        )

        return format(execution)


class GetOutput(command.Command):
    """Show Action execution output data."""

    def get_parser(self, prog_name):
        parser = super(GetOutput, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            help='Action execution ID.')

        return parser

    def take_action(self, parsed_args):
        output = action_executions.ActionExecutionManager(
            self.app.client
        ).get(
            parsed_args.id
        ).output

        try:
            output = json.loads(output)
            output = json.dumps(output, indent=4) + "\n"
        except:
            LOG.debug("Task result is not JSON.")

        self.app.stdout.write(output or "\n")


class GetInput(command.Command):
    """Show Action execution input data."""

    def get_parser(self, prog_name):
        parser = super(GetInput, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            help='Action execution ID.'
        )

        return parser

    def take_action(self, parsed_args):
        result = action_executions.ActionExecutionManager(
            self.app.client
        ).get(
            parsed_args.id
        ).input

        try:
            result = json.loads(result)
            result = json.dumps(result, indent=4) + "\n"
        except:
            LOG.debug("Task result is not JSON.")

        self.app.stdout.write(result or "\n")
