"""
The main.py file handle the starting of the hole server and website.
It takes some arguments :
    bind -- to bind a specific ip to the server
    port -- if you want to use a different port than 80

"""

from api.sport import *

from http import server  # XXX : server.HTTPServer as a placeholder for the future server (think about multithreading)

from web import handler  # Import handler

TEST_PORT = 8008
PROD_PORT = 80

bind = "127.0.0.1"  # Same as localhost or 127.0.0.1
port = TEST_PORT

print("Going to listen at {} on port {}".format("localhost" if bind == "" else bind, port))


class CurrentHandler(handler.ServerHandler):
    def __init__(self, r, ca, s):
        self.api = {"sport": [city.city, activity.activity, installation.installation]}
        self.static = "./static"
        self.notFound = ""

        super().__init__(r, ca, s)


serv = server.HTTPServer((bind, port), CurrentHandler)

try:
    serv.serve_forever()
except KeyboardInterrupt:
    print("\rServer killed, cancel all requests")
