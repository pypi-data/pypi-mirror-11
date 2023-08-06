# -*- coding: utf-8 -*-
# 14-8-8
# create by: snower

import time
from collections import deque
from tornado.concurrent import TracebackFuture
from tornado.ioloop import IOLoop
from .client import Client

class ConnectionPoolClosedError(Exception):pass
class ConnectionNotFoundError(Exception):pass
class ConnectionNotUsedError(Exception):pass
class ConnectionUsedError(Exception):pass

class Connection(Client):
    def __init__(self, pool, *args, **kwargs):
        self._pool = pool
        self.idle_time = time.time()
        super(Connection, self).__init__(*args, **kwargs)

    def close(self, remote_close = False):
        if remote_close:
            return self.do_close()
        return self._pool.release_connection(self)

    def do_close(self):
        return super(Connection, self).close()


class ConnectionPool(object):
    def __init__(self, *args, **kwargs):
        self._max_connections = kwargs.pop("max_connections") if "max_connections" in kwargs else 1
        self._idle_seconds = kwargs.pop("idle_seconds") if "idle_seconds" in kwargs else 0
        self._args = args
        self._kwargs = kwargs
        self._connections = deque()
        self._used_connections = deque()
        self._connections_count = 0
        self._wait_connections = deque()
        self._closed = False
        self._close_future = None
        self._check_idle_callback = False

    def init_connection(self, callback):
        def _(connection_future):
            if connection_future._exc_info is None:
                connection = connection_future._result
                callback(True, connection)
            else:
                callback(False, connection_future._exc_info)
        connection = Connection(self, *self._args, **self._kwargs)
        connection.set_close_callback(self.connection_close_callback)
        self._connections_count += 1
        self._used_connections.append(connection)
        connection_future = connection.connect()
        IOLoop.current().add_future(connection_future, _)

        if self._idle_seconds > 0 and not self._check_idle_callback:
            IOLoop.current().add_timeout(time.time() + self._idle_seconds, self.check_idle_connections)
            self._check_idle_callback = True

    def get_connection(self):
        future = TracebackFuture()
        if self._closed:
            future.set_exception(ConnectionPoolClosedError())
            return future

        if not self._connections:
            if self._connections_count < self._max_connections:
                def _(succed, result):
                    if succed:
                        future.set_result(result)
                    else:
                        future.set_exc_info(result)
                self.init_connection(_)
            else:
                self._wait_connections.append(future)
        else:
            connection = self._connections.popleft()
            self._used_connections.append(connection)
            future.set_result(connection)
        return future

    Connection = get_connection

    def release_connection(self, connection):
        if self._closed:
            return connection.do_close()

        if self._wait_connections:
            future = self._wait_connections.popleft()
            IOLoop.current().add_callback(lambda :future.set_result(connection))
        else:
            try:
                self._used_connections.remove(connection)
                self._connections.append(connection)
                connection.idle_time = time.time()
            except ValueError:
                if connection not in self._connections:
                    connection.do_close()
                    raise ConnectionNotFoundError()
                else:
                    raise ConnectionNotUsedError()

    def close_connection(self, connection):
        try:
            self._connections.remove(connection)
            self._used_connections.append(connection)
            return connection.do_close()
        except ValueError:
            raise ConnectionUsedError()

    def connection_close_callback(self, connection):
        try:
            self._used_connections.remove(connection)
            self._connections_count -= 1
        except ValueError:
            try:
                self._connections.remove(connection)
                self._connections_count -= 1
            except ValueError:
                pass
        if self._close_future and not self._used_connections and not self._connections:
            def do_close():
                self._close_future.set_result(None)
                self._close_future = None
            IOLoop.current().add_callback(do_close)

    def close(self):
        if self._closed:
            raise ConnectionPoolClosedError()

        self._closed = True
        self._close_future = TracebackFuture()

        while len(self._wait_connections):
            future = self._wait_connections.popleft()
            IOLoop.current().add_callback(lambda :future.set_exception(ConnectionPoolClosedError()))

        while len(self._connections):
            connection = self._connections.popleft()
            self._used_connections.append(connection)
            connection.do_close()
        return self._close_future

    def check_idle_connections(self):
        next_check_time = time.time() + self._idle_seconds
        for connection in tuple(self._connections):
            if time.time() - connection.idle_time > self._idle_seconds:
                self.close_connection(connection)
            elif connection.idle_time + self._idle_seconds < next_check_time:
                next_check_time = connection.idle_time + self._idle_seconds

        if not self._closed and self._connections or self._used_connections:
            IOLoop.current().add_timeout(next_check_time, self.check_idle_connections)
        else:
            self._check_idle_callback = False