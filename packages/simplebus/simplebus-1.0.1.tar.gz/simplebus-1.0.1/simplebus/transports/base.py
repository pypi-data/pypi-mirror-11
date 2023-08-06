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

"""Base classes to implement a transport."""


import logging
import time

from abc import ABCMeta
from abc import abstractmethod
from threading import Thread
from ..utils import EventHandler

LOGGER = logging.getLogger(__name__)


class Transport(metaclass=ABCMeta):
    """
    Main base class to a transport.
    This class is used to establish a connection to the broker and
    send/receive messages.
    """

    closed = None

    @property
    @abstractmethod
    def is_open(self):
        """Gets the value that indicates whether the transport is open."""
        pass

    @abstractmethod
    def open(self):
        """Opens the connection to the broker."""
        pass

    @abstractmethod
    def close(self):
        """Closes the connection to the broker."""
        pass

    @abstractmethod
    def cancel(self, id):
        """Cancels from receiving messages from a queue."""
        pass

    @abstractmethod
    def push(self, queue, message, options):
        """Sends a message to the specified queue."""
        pass

    @abstractmethod
    def pull(self, id, queue, callback, options):
        """Starts receiving messages from the specified queue."""
        pass

    @abstractmethod
    def publish(self, topic, message, options):
        """Publishes a message to the specified topic."""
        pass

    @abstractmethod
    def subscribe(self, id, topic, callback, options):
        """Subscribes to receive published messages to the specified topic."""
        pass

    @abstractmethod
    def unsubscribe(self, id):
        """Unsubscribes from receiving published messages from a topic."""
        pass


class TransportMessage(object):
    """An envelope used by SimpleBus to package messages for transmission."""

    def __init__(self, app_id=None,
                 message_id=None,
                 content_type=None,
                 content_encoding=None,
                 body=None,
                 expiration=None):
        self._app_id = app_id
        self._message_id = message_id
        self._content_type = content_type
        self._content_encoding = content_encoding
        self._body = body
        self._expiration = expiration
        self._retry_count = 0
        self._headers = {}

    @property
    def app_id(self):
        """Gets the identifier of the application."""
        return self._app_id

    @app_id.setter
    def app_id(self, value):
        """Sets the identifier of the application."""
        self._app_id = value

    @property
    def message_id(self):
        """Gets the identifier of the message."""
        return self._message_id

    @message_id.setter
    def message_id(self, value):
        """Sets the identifier of the message."""
        self._message_id = value

    @property
    def content_type(self):
        """Gets the type of the content."""
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        """Sets the type of the content."""
        self._content_type = value

    @property
    def content_encoding(self):
        """Gets the encoding of the content."""
        return self._content_encoding

    @content_encoding.setter
    def content_encoding(self, value):
        """Sets the encoding of the content."""
        self._content_encoding = value

    @property
    def body(self):
        """Gets the body as byte array."""
        return self._body

    @body.setter
    def body(self, value):
        """Sets the body as byte array."""
        self._body = value

    @property
    def expiration(self):
        """Gets the expiration in milliseconds."""
        return self._expiration

    @expiration.setter
    def expiration(self, value):
        """Sets the expiration in milliseconds."""
        self._expiration = value

    @property
    def retry_count(self):
        """Gets the number of retries."""
        return self._retry_count

    @property
    def headers(self):
        """Gets the headers."""
        return self._headers

    @headers.setter
    def headers(self, value):
        """Sets the headers."""
        self._headers = value

    def delete(self):
        """Deletes this message from the broker."""
        pass

    def dead_letter(self, reason):
        """Deliveries this message to the specified dead letter queue."""
        pass

    def retry(self):
        """Redelivery this message to be processed again."""
        pass


class RecoveryAwareTransport(Transport):
    """
    Transport that provides auto reconnection for a base transport.
    """

    def __init__(self, transport, recovery_min_delay, recovery_delta_delay, recovery_max_delay):
        self.__is_open = False
        self.__cancellations = {}
        self.__subscriptions = {}
        self.__recovery_min_delay = recovery_min_delay
        self.__recovery_delta_delay = recovery_delta_delay
        self.__recovery_max_delay = recovery_max_delay
        self.__transport = transport
        self.__transport.closed += self.__on_closed
        self.closed = EventHandler()

    @property
    def is_open(self):
        """Gets the value that indicates whether the transport is open."""

        return self.__is_open

    def open(self):
        """Opens the connection to the broker."""

        self.__transport.open()
        self.__is_open = True

    def close(self):
        """Closes the connection to the broker."""

        self.__transport.close()
        self.__is_open = False

    def cancel(self, id):
        """Cancels from receiving messages from a queue."""

        cancellation = self.__cancellations.pop(id)
        if cancellation:
            self.__transport.cancel(id)

    def push(self, queue, message, options):
        """Sends a message to the specified queue."""

        self.__transport.push(queue, message, options)

    def pull(self, id, queue, callback, options):
        """Starts receiving messages from the specified queue."""

        self.__cancellations[id] = dict(id=id, queue=queue, callback=callback, options=options)
        self.__transport.pull(id, queue, callback, options)

    def publish(self, topic, message, options):
        """Publishes a message to the specified topic."""

        self.__transport.publish(topic, message, options)

    def subscribe(self, id, topic, callback, options):
        """Subscribes to receive published messages to the specified topic."""

        self.__subscriptions[id] = dict(id=id, topic=topic, callback=callback, options=options)
        self.__transport.subscribe(id, topic, callback, options)

    def unsubscribe(self, id):
        """Unsubscribes from receiving published messages from a topic."""

        subscriber = self.__subscriptions.pop(id)
        if subscriber:
            self.__transport.unsubscribe(id)

    def __on_closed(self, by_user):
        """Called when the base transport is closed unexpected."""

        self.closed(by_user)

        if not by_user:
            self.__start_recovery()

    def __recover(self):
        """Tries to reconnect to the broker."""

        count = 1
        while self.is_open and not self.__transport.is_open:
            try:
                LOGGER.warn('Attempt %s to reconnect to the broker.' % count)
                self.__transport.open()
                self.__recover_cancellations()
                self.__recover_subscriptions()
                LOGGER.info('Connection re-established to the broker.')
            except:
                delay = (2*(count-1)) * self.__recovery_delta_delay + self.__recovery_min_delay
                if delay > self.__recovery_max_delay:
                    delay = self.__recovery_max_delay
                time.sleep(delay)
                count += 1

    def __recover_cancellations(self):
        """Starts pulling again all queues that were being pulled."""

        for cancellation in self.__cancellations.values():
            try:
                self.pull(**cancellation)
            except:
                LOGGER.critical('Recovering failed for the  %s.' %
                                cancellation.get('queue'), exc_info=True)

    def __recover_subscriptions(self):
        """Subscribes again all topics that were subscribed."""

        for subscription in self.__subscriptions.values():
            try:
                self.subscribe(**subscription)
            except:
                LOGGER.critical('Recovering failed for the topic %s.' %
                                subscription.get('topic'), exc_info=True)

    def __start_recovery(self):
        """Starts recovery of transport."""

        thread = Thread(target=self.__recover)
        thread.daemon = True
        thread.start()
