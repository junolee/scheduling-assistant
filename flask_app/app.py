# coding: utf-8
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse

PORT_NUMBER = 8080

#This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        msg = query_components["message"]
        self.wfile.write(msg)
        return

if __name__ == '__main__':
    try:
    	#Create a web server and define the handler to manage the
    	#incoming request
    	server = HTTPServer(('', PORT_NUMBER), myHandler)
    	print 'Started httpserver on port ' , PORT_NUMBER

    	#Wait forever for incoming http requests
    	server.serve_forever()

    except KeyboardInterrupt:
    	print '^C received, shutting down the web server'
    	server.socket.close()
