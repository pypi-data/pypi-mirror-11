#
# growler/http/protocol.py
#
"""
Code containing Growler's asyncio.Protocol code for handling HTTP requests.
"""

from growler.protocol import GrowlerProtocol
from growler.http.responder import GrowlerHTTPResponder
from growler.http.response import HTTPResponse
from growler.http.errors import (
    HTTPError,
    HTTPErrorInternalServerError
)

import asyncio
import traceback
import sys


# Or should this be called HTTPGrowlerProtocol?
class GrowlerHTTPProtocol(GrowlerProtocol):
    """
    GrowlerProtocol dealing with HTTP requests. Objects are created with a
    growler.App instance, which contains the relevant event_loop. The default
    responder_type is GrowlerHTTPResponder, which does the data parsing and
    req/res creation.
    """

    def __init__(self, app):
        """
        Construct a GrowlerHTTPProtocol object. This should only be called from
        a growler.HTTPServer instance (or any asyncio.create_server function).

        @param app: Typically a growler application which is the 'endpoint' for
            this protocol, but any callable with a 'loop' attribute should
            work.
        """
        print("[GrowlerHTTPProtocol::__init__]", id(self))

        def responder_factory(_self):
            return GrowlerHTTPResponder(_self,
                                        request_factory=app._request_class,
                                        response_factory=app._response_class)

        super().__init__(loop=app.loop, responder_factory=responder_factory)
        self.http_application = app

    def middleware_chain(self, req, res):
        """
        Runs through the chain of middleware in app.
        """
        for mw in self.http_application.middleware_chain(req):
            try:
                if asyncio.iscoroutine(mw):
                    print("Running middleware coroutine:", mw)
                    self.loop.run_until_complete(mw(req, res))
                else:
                    print("Running middleware:", mw)
                    mw(req, res)
                print(" -> DONE")
            except Exception as error:
                print(" -> EXCEPTION OCCURED", error)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=5, file=sys.stdout)
                # print(inspect.stack())
                for handler in self.http_application.next_error_handler(req):
                    handler(req, res, error)
                return

        if not res.has_ended:
            raise HTTPErrorInternalServerError

    def handle_error(self, error):
        """
        An error handling function which will be called when an error is raised
        during a responder's on_data() function. There is no default
        functionality and the subclasses must overload this.

        @param error: Exception thrown in code
        """
        # for error_handler in self.http_application.next_error_handler(req):
        if isinstance(error, HTTPError):
            err_str = ("<html>"
                       "<head></head>"
                       "<body><h1>HTTP Error : %d %s </h1></body>"
                       "</html>") % (error.code, error.msg)
            header_info = {
                'code': error.code,
                'msg': error.msg,
                'date': HTTPResponse.get_current_time(),
                'length': len(err_str.encode()),
                'contents': err_str
            }
            response = ("HTTP/1.1 {code} {msg}\n"
                        "Content-Type: text/html; charset=UTF-8"
                        "Content-Length: {length}"
                        "Date: {date}\n\n"
                        "{contents}").format(**header_info)
            self.transport.write(response.encode())
