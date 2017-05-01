#!/usr/bin/pythonRoot

from flup.server.fcgi import WSGIServer
import sys, urlparse

def app(environ, start_response):
	start_response("200 OK", [("Content-Type", "text/html")])
	i = urlparse.parse_qs(environ["QUERY_STRING"])
	yield ('blargh ')

WSGIServer(app).run()
