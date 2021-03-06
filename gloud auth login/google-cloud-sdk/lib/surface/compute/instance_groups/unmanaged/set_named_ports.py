# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""instance-groups unmanaged set-named-ports command.

It's an alias for the instance-groups set-named-ports command.
"""
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import instance_groups_utils
from googlecloudsdk.command_lib.compute import flags as compute_flags
from googlecloudsdk.command_lib.compute import scope as compute_scope
from googlecloudsdk.command_lib.compute.instance_groups import flags


class SetNamedPorts(base_classes.NoOutputAsyncMutator):
  """Sets named ports for instance groups."""

  @property
  def service(self):
    return self.compute.instanceGroups

  @property
  def method(self):
    return 'SetNamedPorts'

  @property
  def resource_type(self):
    return 'instanceGroups'

  @staticmethod
  def Args(parser):
    flags.AddNamedPortsArgs(parser)
    flags.ZONAL_INSTANCE_GROUP_ARG.AddArgument(parser)

  def CreateRequests(self, args):
    group_ref = (
        flags.ZONAL_INSTANCE_GROUP_ARG.ResolveAsResource(
            args, self.resources,
            default_scope=compute_scope.ScopeEnum.ZONE,
            scope_lister=compute_flags.GetDefaultScopeLister(
                self.compute_client)))
    ports = instance_groups_utils.ValidateAndParseNamedPortsArgs(
        self.messages, args.named_ports)
    # service should be always zonal
    request, _ = instance_groups_utils.GetSetNamedPortsRequestForGroup(
        self.compute_client, group_ref, ports)
    return [(self.service, self.method, request)]

  detailed_help = instance_groups_utils.SET_NAMED_PORTS_HELP
