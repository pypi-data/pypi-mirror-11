#
# growler/http/server.py
#
"""
Functions and classes for running an http server
"""

import asyncio
from ssl import SSLContext
from types import GeneratorType

from .protocol import GrowlerHTTPProtocol


def create_server(
        callback=None,
        host='127.0.0.1',
        port=8000,
        ssl=None,
        loop=None,
        **kargs
        ):
    """
    This is a function to assist in the creation of a growler HTTP server.

    @param host str: hostname or ip address on which to bind
    @param port: the port on which the server will listen
    @param ssl ssl.SSLContext: The SSLContext for using TLS over the connection
    @param loop asyncio.BaseEventLoop: The event loop to
    @param kargs: Extra parameters passed to the HTTPServer instance created.
                  If there is an ssl parameter passed to this function, kargs
                  will require the value 'key' to be present, and an optional
                  'cert' parameter to pass to load_cert_chain.
    @return An HTTPServer instance
    """

    loop = asyncio.get_event_loop() if loop is None else loop

    if ssl:
        sslctx = SSLContext(ssl.PROTOCOL_SSLv23)
        key = kargs.pop('key')
        try:
            sslctx.load_cert_chain(certfile=kargs.pop('cert'), keyfile=key)
        except KeyError:
            sslctx.load_cert_chain(certfile=key)
    else:
        sslctx = None

    # What do I use as a 'callback' here?
    srv = HTTPServer(cb=callback,
                     loop=loop,
                     ssl=sslctx,
                     host=host,
                     port=port,
                     **kargs
                     )
    return srv


class HTTPServer():
    """
    This is the reference implementation of an HTTP server for the Growler
    project.
    The server itself behaves as a proxy for the asyncio coroutine that the
    user will actualy want to use. The server is not given a lot of state:
    standard server information: host, port, ssl which are given to the
    asyncio.create_server() function.
    """

    def __init__(self,
                 cb=None,
                 host='0.0.0.0',
                 port='8000',
                 sockfile=None,
                 loop=None,
                 ssl=None,
                 **kargs):
        """
        Construct a server. Parameters given here will be forwarded to the
        asyncio.create_server function.

        @param cb runnable: The callback to handle requests
        @param host str: hostname or ip address on which to bind
        @param port: the port on which the server will listen. If port is a
            tuple of numbers, it randomly select an available port between them
            domain: [port[0], port[1]). If port is a callable, it will run it,
            cast the result to an int, and set this to 'port'.
        @param sockfile str: A filename which will act as a unix file socket
            for communication with the server. If this is set, the server will
            NOT listen on a port and will take this value. If host or port are
            set at a later time, the socket attribute is removed and it will
            listen on that.
        @param loop asyncio.event_loop: the event loop this server is using. If
            none it will default to asyncio.get_event_loop
        @param ssl ssl.SSLContext: If not none, we are hosting HTTPS
        @param kargs: Any extra arguments to be given to the server
        """
        self.callback = cb
        self.loop = loop or asyncio.get_event_loop()
        self.ssl = ssl
        self.server_options = dict()

        if isinstance(port, tuple):
            port = self.get_random_port(port)
        elif isinstance(port, GeneratorType):
            for p in port:
                if self.port_is_open(p):
                    break
            else:
                raise Exception("Could not find an open port from generator %s"
                                % port)
            port = p
        elif callable(port):
            port = int(port())

        # presence of 'sockfile' takes precedence over host/port
        if sockfile is not None:
            self.server_options['sockfile'] = sockfile
        else:
            self.host = host
            self.port = port

        self._saved_host = host
        self._saved_port = port

        self.proto_args = dict()
        self.kargs = kargs

    @property
    def port(self):
        return self.server_options['port']

    @port.setter
    def port(self, port):
        if self.server_options.pop('sockfile', None) is not None:
            self.server_options['host'] = self._saved_host
        self.server_options['port'] = int(port)

    @property
    def host(self):
        return self.server_options['host']

    @host.setter
    def host(self, host):
        if self.server_options.pop('sockfile', None) is not None:
            self.server_options['port'] = self._saved_port
        self.server_options['host'] = host

    @property
    def unix_socket(self):
        return self.server_options['sockfile']

    @unix_socket.setter
    def unix_socket(self, sock):
        """
        Set the unix_socket the server should (create) listen to. If host and
        port are present, remove them from server_options, but save them just
        in case.
        """
        p = self.server_options.pop('port', None)
        h = self.server_options.pop('host', None)
        if p is not None:
            self._saved_port = p
        if h is not None:
            self._saved_host = h
        self.server_options['sockfile'] = sock

    def serve_forever(self):
        """
        Simply calls the event loop's run forever method.
        """
        self.loop.run_forever()

    def listen(self, port=None, host=None, socket_file=None, block=False):
        """
        Method to indicate to the server to listen on a particular port.

        @param host str: hostname or ip address to listen on. If None it will
            use the value stored in self.host
        @param port int: The port number to listen on. If None the server will
            use the value stored in self.port
        @param socket_file str: A path to create a unix socket file on, if this
            is set, host and port parameters are ignored
        @param block bool: If true, this function will run until the server
            stops running.
        @return The asyncio.coroutine which is created by a call to
            asyncio.create_server
        """

        # Update values if specified
        if socket_file is not None:
            self.unix_socket = socket_file
        else:
            if port is not None:
                self.port = port
            if host is not None:
                self.host = host

        #
        self._coro = self.loop.create_server(
            self.generate_protocol,
            **self.server_options
            )
        if block:
            self.loop.run_until_complete(self.coro)
            print('Listening : {}'.format(self.srv.sockets[0].getsockname()))
            print(' sock {}'.format(self.srv.sockets[0]))
            self.loop.run_forever()
        return self._coro

    def generate_protocol(self):
        """
        Helper function to act as a protocol factory for the
        GrowlerHTTPProtocol
        """
        return GrowlerHTTPProtocol(app=self.callback)

    def __call__(self, **kargs):
        """
        Calling a server object returns a coroutine created from a call to
        asyncio.BaseEventLoop.create_server, this coroutine can be wrapped in a
        task or called however the user wishes.
        """
        return self.loop.create_server(self.generate_protocol,
                                       **self.server_kargs)

    @classmethod
    def get_random_port(cls, range_tuple, MAX_TRIES=200):
        """
        Return a port selected randomly the range provided.

        @param range_tuple: tuple of two integers, between which the port will
                            be selected. The numbers are generated from the
                            standard library's random.randrange function.
        @param MAX_TRIES: Number of total attempts the loop will run before
                          giving up.
        """
        import socket
        import random
        low, high = int(range_tuple[0]), int(range_tuple[1])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for counter in range(0, min(high-low, MAX_TRIES)):
            test_port = random.randrange(low, high)
            if HTTPServer.port_is_open(test_port, s):
                return test_port
        err_str = "Could not find random port in range {}"
        raise Exception(err_str.format(range_tuple))

    @staticmethod
    def port_is_open(test_port, sock=None, host='0.0.0.0'):
        """
        Helper function which determines if a port is available. Attempts to
        open a socket on hostname 'host' on the port provided, if connection is
        refused, assume the port is open. A socket can be provided so the a new
        one does not have to be created at every run.
        @param test_port int: The port to test
        @param sock: Optional socket on which to run the test.
        @param host: The host the function attempts to connect to.
        """
        import socket
        CONNECTION_REFUSED = (111, 61)
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        is_open = sock.connect_ex((host, test_port)) in CONNECTION_REFUSED
        sock.close()
        return is_open
