"""
handler.py create a class server that implement BaseHTTPRequestHandler.
    static -- the path to server static file (in case the requested path is not an api)
    api -- a list of implementation of "route"
"""
import http.server

import shutil
import os
import urllib
import posixpath
import re

class serverHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, r, ca, s):
        # TODO : assert that api has the form {subapi:{api1, api2, ...}, subapi2:[apiN, ...]} and that they all implement BaseRestAPI


        # XXX : It should be coded differently
        self.static = "./static" # static # Absolute path to the static part of the website
        self.api = {} # api # Dictionary containing all the api that should be used/served
        self.notfound = "" # staticnotfound # Absolute path to a 404 display

        super().__init__(r, ca, s)

    # Starting def of REST HTTP methods
    def do_GET(self):
        self.handleReq("GET")

    def do_PUT(self):
        self.handleReq("PUT")

    def do_POST(self):
        self.handleReq("POST")

    def do_DELETE(self):
        handleReq("DELETE")

    def handleReq(self, proto):
        print(self.path)
        if(isAPI(self.path)):
            self.handleAPI(proto)
        else:
            self.serve()

    def serve(self):
        # Retrieve a path to the file and parse things like "/../", "/./" or "//"
        filepath = posixpath.normpath(urllib.parse.unquote(self.path))
        source = self.static
        sourcefile = None
        # Root of the website
        if filepath == '/':
            filepath += "index.html"

        # If its a directory (not the root) return a 404
        if filepath[-1] == '/':
            self.do404()
            return

        # Add the requested path to the absolute static path
        for dirs in filter(None, filepath.split("/")):
            source = os.path.join(source, dirs)

        try :
            sourcefile = open(source, "rb")
        except Exception:
            # File not found or denied
            self.do404()
            return

        self.send_response(200)
        # TODO : Add the header line : Content-Type (parsing needed)
        self.end_headers()

        shutil.copyfileobj(sourcefile, self.wfile)

    def do404(self):
        self.send_response(404)
        self.end_headers()
        shutil.copyfileobj(open(self.notfound, "rb"), self.wfile)

    def handleAPI(self, proto):
        # Be sure that we respect the form /api/sub/resource so 3 items
        # filter is used to abstract any useless "/" at the begining of double "/"
        path = list(filter(None, self.path.split("/")))

        if (len(path) != 3):
            # fail so we return a "400 : bad request" code
            self.send_error(400, "Malformed API call")
            return

        subAPIName, apiName = path[1:]

        """ try to find the api
            first  "in" looks if there is the sub_api
            second "in" retrieve classes names in the sub api and compare it to the ressource
        """
        if (subAPIName in self.api and apiName in [api.__name__ for api in self.api[subAPIName]]):
            subAPI = self.api[subAPIName]
            api = [api for api in subAPI if api.__name__ == apiName][0]
            # Look for a support for the method in the api
            if (proto not in api.supported):
                self.send_header("Allow", ", ".join(api.supported))
                self.send_error(405, "Method not allowed")
                return
            # Here all preliminary checks are done
            run = getattr(api, proto);
            result = run(self.rfile)

            # Start of header
            self.send_header("Content-type", result["content"])
            for h in result["header"]:
                # h structure : (header name, header content)
                self.send_header(h[0], h[1])
            self.send_response(result["code"])
            self.end_headers()

            # Start of content
            self.wfile.write( result["res"] )

            # That it !

        else:
            # The API does not exist nor stored
            self.send_error(501, "API is not implemented yet")



def isAPI(urlpath):
    return bool(re.match(r'^/api/.*$', urlpath))
