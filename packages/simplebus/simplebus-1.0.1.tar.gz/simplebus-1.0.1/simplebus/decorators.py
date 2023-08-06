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

"""Implements the decorator methods."""


from .state import current_bus


def pull(queue, **options):
    """Starts receiving messages from the specified queue."""

    def decorator(cls_or_func):
        current_bus.pull(queue, cls_or_func, **options)
        return cls_or_func
    return decorator


def subscribe(topic, **options):
    """Subscribes to receive published messages to the specified topic."""

    def decorator(cls_or_func):
        current_bus.subscribe(topic, cls_or_func, **options)
        return cls_or_func
    return decorator
