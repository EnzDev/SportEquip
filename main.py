"""
The main.py file handle the starting of the hole server and website.
It takes some arguments :
    bind -- to bind a specific ip to the server
    port -- if you want to use a different port than 80

"""

from web import * # Import the server (TODO) and his handler
from api import * # Import the API that will be given to the server


from http import server # XXX : server.HTTPServer as a placeholder for the future server (think about multithreading)

TEST_PORT = 8080
PROD_PORT = 80

bind = "" # Same as localhost or 127.0.0.1
port = TEST_PORT

print( "Going to listen at {} on port {}".format("localhost" if bind=="" else bind, port) )

serv = server.HTTPServer((bind, port), handler.serverHandler)
try:
    serv.serve_forever()
except KeyboardInterrupt:
    print("\rServer killed, cancel all requests")
