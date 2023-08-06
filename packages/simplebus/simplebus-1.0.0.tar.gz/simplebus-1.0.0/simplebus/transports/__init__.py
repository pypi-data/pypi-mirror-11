# Copyright 2015 Vinicius Chiele. All rights reserved.
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

from ..transports.base import RecoveryAwareTransport
from ..utils import import_string


TRANSPORT_ALIASES = {
    'amqp': 'simplebus.transports.amqp.Transport',
}


def create_transport(url, recovery_enabled, recovery_min_delay, recovery_delta_delay, recovery_max_delay):
    if '://' not in url:
        raise ValueError('Invalid url %s.' % url)

    schema = url.partition('://')[0]

    class_name = TRANSPORT_ALIASES.get(schema)

    if class_name is None:
        raise ValueError('Invalid schema %s.' % schema)

    transport_cls = import_string(class_name)

    transport = transport_cls(url)

    if not recovery_enabled:
        return transport

    if recovery_min_delay < 0:
        raise ValueError('recovery_min_delay should be greater or equal to 0')

    if recovery_min_delay > recovery_max_delay:
        raise ValueError('recovery_min_delay should be less or equal to recovery_max_delay')

    if recovery_delta_delay < 1:
        raise ValueError('recovery_delta_delay should be greater than 0')

    return RecoveryAwareTransport(transport, recovery_min_delay, recovery_delta_delay, recovery_max_delay)
