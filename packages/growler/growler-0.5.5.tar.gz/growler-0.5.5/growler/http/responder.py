#
# growler/http/responder.py
#
"""
The Growler class responsible for responding to HTTP requests.
"""

from .parser import Parser
from .request import HTTPRequest
from .response import HTTPResponse

from .errors import (
    HTTPErrorBadRequest
)


class GrowlerHTTPResponder():
    """
    The Growler Responder for HTTP connections. This class responds to incoming
    connections by parsing the incoming data as as ah HTTP request (using
    functions in growler.http.parser) and creating request and response objects
    which are finally passed to the app object found in protocol.
    """

    def __init__(self,
                 protocol,
                 parser_factory=Parser,
                 request_factory=HTTPRequest,
                 response_factory=HTTPResponse
                 ):
        """
        Construct an HTTPResponder.

        This should only be called from a growler protocol instance.

        @param protocol: The GrowlerHTTPProtocol which created the responder.
        """
        self._proto = protocol
        self.loop = protocol.loop
        self.parser = parser_factory(self)
        self.endpoint = protocol.http_application
        self.build_req = request_factory
        self.build_res = response_factory
        self.headers = None

    def on_data(self, data):
        """
        This is the function called by the http protocol upon receipt of
        incoming client data.
        """
        # Headers have not been read in yet
        if self.headers is None:
            # forward data to the parser
            data = self.parser.consume(data)

            # Headers are finished - build the request and response
            if data is not None:
                self.build_req_res()
                # self.loop.call_soon(self._proto.middleware_chain)
                self._proto.middleware_chain(self.req, self.res)

        # if truthy, 'data' now holds body data
        if data:
            self.validate_and_store_body_data(data)

            # if we have reached end of content - put in the request's body
            if self.content_length == self.headers['CONTENT-LENGTH']:
                self.req.body.set_result(b''.join(self.body_buffer))

    def set_request_line(self, method, url, version):
        """
        Sets the request line on the responder.
        """
        self.parsed_request = (method, url, version)
        self._proto.request = {
            'method': method,
            'url': url,
            'version': version
            }
        if method in ('POST', 'PUT'):
            self.content_length = 0

    def set_headers(self, headers):
        """
        Sets the headers attribute and triggers the beginning of the req/res
        construction.
        """
        self.headers = headers

    def build_req_res(self):
        self.req = self.build_req(self._proto, self.headers)
        self.res = self.build_res(self._proto)
        return self.req, self.res

    def validate_and_store_body_data(self, data):
        """
        Attempts simple body data validation by comparining incoming data to
        the content length header. If passes store the data into self._buffer.
        """
        try:
            maxlen = self.headers['CONTENT-LENGTH']
        except KeyError:
            raise HTTPErrorBadRequest

        try:
            self.content_length += len(data)
        except AttributeError:
            raise HTTPErrorBadRequest

        if self.content_length > maxlen:
            raise HTTPErrorBadRequest

        self.body_buffer.append(data)
