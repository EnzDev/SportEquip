"""
handler.py create a class server that implement BaseHTTPRequestHandler.
    static -- the path to server static file (in case the requested path is not an api)
    api -- a list of implementation of "route"
"""
import cgi
import http.server

import shutil
import os
import urllib
import posixpath
import re


class ServerHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, r, ca, s):
        # TODO : assert that api has the form {subapi:[api1, api2, ...], subapi2:[apiN, ...]} and that they all implement BaseRestAPI

        # If values has not been overrode :
        if not hasattr(self, "static"):
            self.static = "./static"  # Absolute path to the static part of the website
        if not hasattr(self, "api"):
            self.api = {}  # Dictionary containing all the api that should be used/served
        if not hasattr(self, "notFound"):
            self.notFound = ""  # path to a 404 display

        super().__init__(r, ca, s)

    # Starting def of REST HTTP methods
    def do_GET(self):
        self.handleReq("get")

    def do_PUT(self):
        self.handleReq("put")

    def do_POST(self):
        self.handleReq("post")

    def do_DELETE(self):
        self.handleReq("delete")

    def handleReq(self, proto):
        # print(self.path)
        if isApi(self.path):
            self.handleAPI(proto)
        else:
            self.serve()

    def serve(self):
        # Retrieve a path to the file and parse things like "/../", "/./" or "//"
        filepath = posixpath.normpath(urllib.parse.unquote(self.path))
        source = self.static

        # Root of the website
        if filepath == '/':
            filepath += "index.html"

        # If its a directory (not the root) return a 404
        if filepath[-1] == '/':
            self.do404("Empty folder")
            return

        # Add the requested path to the absolute static path
        for dirs in filter(None, filepath.split("/")):
            source = os.path.join(source, dirs)

        try:
            sourcefile = open(source, "rb")
        except FileNotFoundError:
            # File not found or denied
            self.do404(filepath)
            return

        self.send_response(200)
        # TODO : Add the header line : Content-Type (parsing needed)
        self.end_headers()

        shutil.copyfileobj(sourcefile, self.wfile)

    def do404(self, filename):
        self.send_response(404)
        self.end_headers()
        try:
            shutil.copyfileobj(open(self.notFound, "rb"), self.wfile)
        except FileNotFoundError:  # In case the 404 page is not defined..
            self.wfile.write(str.encode("Fichier non trouvé... (" + filename + ")"))

    def handleAPI(self, proto):
        # Be sure that we respect the form /api/sub/resource so 3 items
        # filter is used to abstract any useless "/" at the begining of double "/"
        path = list(filter(None, urllib.parse.urlparse(self.path).path.split("/")))

        if len(path) != 3:
            # fail so we return a "400 : bad request" code
            self.send_error(400, "Malformed API call")
            return

        subAPIName, apiName = path[1:]

        """ try to find the api
            first  "in" looks if there is the sub_api
            second "in" retrieve classes names in the sub api and compare it to the ressource
        """
        if subAPIName in self.api and apiName in [api.__name__ for api in self.api[subAPIName]]:
            subAPI = self.api[subAPIName]
            api = [api for api in subAPI if api.__name__ == apiName][0]()  # () to instanciate the class
            # Look for a support for the method in the api
            if proto not in api.supported:
                self.send_error(405, "Method not allowed")
                # FIXME : mmmmh since python 3.3.X the code must be sent before header -> problems
                # self.send_header("Allow: " + ", ".join(api.supported))
                return
            # Here all preliminary checks are done
            run = getattr(api, proto)

            # All the info the APIs can exploit
            infos = {
                "query": dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query)),  # Parse the query
                "method": self.command,
                "client": self.client_address,
                "headers": sorted(self.headers.items()),
                "data": cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': self.command,
                             'CONTENT_TYPE': self.headers['Content-Type'],
                             }
                )
            }

            result = run(infos)

            if type(result) == tuple:  # as defined in BaseApi
                self.send_error(result[0], result[1])
                print("error")

            try:
                # Start of header
                self.send_response(result["code"])
                self.send_header("Content-type", result["content"])
                for h in result["header"]:
                    # h structure : (header name, header content)
                    self.send_header(h[0], h[1])
                self.end_headers()

                # Start of content
                self.wfile.write(result["res"])
                return
            except Exception:
                self.send_error(500, "Internal error during the treatment of the request")
            # That it !

        else:
            # The API does not exist nor stored
            self.send_error(501, "API is not implemented yet")


def isApi(urlpath):
    return bool(re.match(r'^/api/.*$', urlpath))
