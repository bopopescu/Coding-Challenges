# -*- coding: utf-8 -*- #
# Copyright 2018 Google LLC. All Rights Reserved.
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
"""Describe node group command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute import flags as compute_flags
from googlecloudsdk.command_lib.compute.sole_tenancy.node_groups import flags


class Describe(base.DescribeCommand):
  """Describes a Google Compute Engine node group."""

  @staticmethod
  def Args(parser):
    flags.MakeNodeGroupArg().AddArgument(parser)

  def Run(self, args):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client

    node_group_ref = flags.MakeNodeGroupArg().ResolveAsResource(
        args, holder.resources,
        scope_lister=compute_flags.GetDefaultScopeLister(holder.client))

    messages = holder.client.messages
    request = messages.ComputeNodeGroupsGetRequest(
        nodeGroup=node_group_ref.Name(),
        project=node_group_ref.project,
        zone=node_group_ref.zone)

    service = holder.client.apitools_client.nodeGroups
    return client.MakeRequests([(service, 'Get', request)])[0]
