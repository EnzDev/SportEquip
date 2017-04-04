"""
The main.py file handle the starting of the hole server and website.
It takes some arguments :
    bind -- to bind a specific ip to the server
    port -- if you want to use a different port than 80

"""

from api.sport import *

import argparse

from http import server  # XXX : server.HTTPServer as a placeholder for the future server (think about multithreading)

from web import handler  # Import handler

TEST_PORT = 8008
PROD_PORT = 80

TEST_BIND = "127.0.0.1"
PROD_BIND = "0.0.0.0"


bind = TEST_BIND # Same as localhost or 127.0.0.1
port = TEST_PORT



# Arguments to customise the launch (as described when launching with -h or --help)
parser = argparse.ArgumentParser(prog="python3 main.py")

parser.add_argument('--port', type=int, help="Port to listen")
parser.add_argument('--bind', help="Adresse to bind")

g = parser.add_mutually_exclusive_group()

g.add_argument('--dev', help="Use dev parammeters (default)", action="store_true")
g.add_argument('--prod', help="Use production parammeters (must be root)", action="store_true")

arg = parser.parse_args()

if(arg.prod):
    port = PROD_PORT
    bind = PROD_BIND

if(arg.dev):
    port = TEST_PORT
    bind = TEST_BIND

if(arg.port):
    port = arg.port

if(arg.bind):
    bind = arg.bind




print("Going to listen at {} on port {}".format("localhost" if bind == "" else bind, port))


class CurrentHandler(handler.ServerHandler): # We override the handler to setup the APIs functions
    def __init__(self, r, ca, s):
        self.api = {"sport": [city.city, activity.activity, installation.installation]} # Declaration of the functions
        self.static = "./static" # Where the statics file will be served
        self.notFound = "" # A 404 page, if not defined it will be a classic error page

        super().__init__(r, ca, s)


serv = server.HTTPServer((bind, port), CurrentHandler) # Setup the server with the arguments parameters

try:
    serv.serve_forever() # Effectivly launch the server
except KeyboardInterrupt:
    print("\rServer killed, cancel all requests")
