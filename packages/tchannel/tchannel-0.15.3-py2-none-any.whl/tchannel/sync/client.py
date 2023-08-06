# Copyright (c) 2015 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import

from collections import namedtuple
from concurrent.futures import TimeoutError

from threadloop import ThreadLoop
from tornado import gen

from tchannel import tornado as async
from tchannel.tornado.hyperbahn import FIRST_ADVERTISE_TIME, AdvertiseError


class TChannelSyncClient(object):
    """Make synchronous TChannel requests.

    This client does not support incoming connections or requests- this is
    a uni-directional client only.

    The client is implemented on top of the Tornado-based implementation and
    starts and stops IOLoops on-demand.

    .. code-block:: python

        client = TChannelSyncClient()
        response = client.request(
            hostport='localhost:4040',
            service='HelloService',
        ).send(
            'hello', None, json.dumps({"name": "World"})
        )

    """

    def __init__(self, name, process_name=None, known_peers=None, trace=False):
        """Initialize a new TChannelClient.

        :param process_name:
            Name of the calling process. Used for logging purposes only.
        """
        self._async_client = async.TChannel(
            name,
            process_name=process_name,
            known_peers=known_peers,
            trace=trace
        )
        self._threadloop = ThreadLoop()
        self._threadloop.start()

    def request(self, *args, **kwargs):
        """Initiate a new request to a peer.

        :param hostport:
            If specified, requests will be sent to the specific host.
            Otherwise, a known peer will be picked at random.
        :param service:
            Name of the service being called. Defaults to an empty string.
        :param service_threshold:
            If ``hostport`` was not specified, this specifies the score
            threshold at or below which peers will be ignored.
        :returns SyncClientOperation:
            An object with a ``send(arg1, arg2, arg3)`` operation.
        """
        operation = self._async_client.request(*args, **kwargs)
        operation = SyncClientOperation(operation, self._threadloop)

        return operation

    def advertise(self, routers, name=None, timeout=None):
        """Advertise with Hyperbahn.

        :param routers: list of hyperbahn addresses to advertise to.
        :param name: service name to advertise with.
        :param timeout: backoff period for failed requests.
        :returns: first advertise result.
        :raises AdvertiseError: when unable to begin advertising.
        """

        @gen.coroutine
        def make_request():

            response = yield self._async_client.advertise(
                routers=routers,
                name=name,
                timeout=timeout,
            )

            header = yield response.get_header()
            body = yield response.get_body()

            result = Response(header, body)

            raise gen.Return(result)

        future = self._threadloop.submit(make_request)

        # we're going to wait 1s longer than advertises
        # timeout mechanism, so it has a chance to timeout
        wait_until = timeout or FIRST_ADVERTISE_TIME
        wait_until += 1

        # block for advertise's first response,
        # using wait_until as a fallback timeout mechanism
        try:
            result = future.result(wait_until)
        except TimeoutError:
            raise AdvertiseError(
                "Failed to register with Hyperbahn."
            )

        return result


class SyncClientOperation(object):
    """Allows making client operation requests synchronously.

    This object acts like tchannel.TChannelClientOperation, but instead
    uses a threadloop to make the request synchronously.
    """

    def __init__(self, operation, threadloop):
        assert operation, "operation is required"
        assert threadloop, "threadloop.ThreadLoop is required"
        self.operation = operation
        self._threadloop = threadloop

    def send(self, arg1, arg2, arg3):
        """Send the given triple over the wire.

        :param arg1:
            String containing the contents of arg1. If None, an empty string
            is used.
        :param arg2:
            String containing the contents of arg2. If None, an empty string
            is used.
        :param arg3:
            String containing the contents of arg3. If None, an empty string
            is used.
        :return concurrent.futures.Future:
            Future response from the peer.
        """
        arg1 = arg1 or ''
        arg2 = arg2 or ''
        arg3 = arg3 or ''

        @gen.coroutine
        def make_request():

            response = yield self.operation.send(arg1, arg2, arg3)

            header = yield response.get_header()
            body = yield response.get_body()

            result = Response(header, body)

            raise gen.Return(result)

        future = self._threadloop.submit(make_request)
        return future


Response = namedtuple('Response', 'header, body')
