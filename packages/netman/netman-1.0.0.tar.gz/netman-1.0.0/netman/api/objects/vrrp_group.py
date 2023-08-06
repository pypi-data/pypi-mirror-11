# Copyright 2015 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from netaddr import IPNetwork

from netman.api.serializer import Serializer
from netman.core.objects.vrrp_group import VrrpGroup


class SerializableVrrpGroup(Serializer):
    def __init__(self, src):
        super(SerializableVrrpGroup, self).__init__(['id', 'ips', 'hello_interval', 'dead_interval', 'priority',
                                                     'track_id', 'track_decrement'])
        self.id = src.id
        self.ips = sorted([ipn.ip.format() for ipn in src.ips])
        self.priority = src.priority
        self.track_id = src.track_id
        self.track_decrement = src.track_decrement
        self.hello_interval = src.hello_interval
        self.dead_interval = src.dead_interval

    @classmethod
    def to_core(cls, **serialized):
        ips = serialized.pop('ips')
        return VrrpGroup(
            ips=[IPNetwork(ip) for ip in ips],
            ** serialized
        )
