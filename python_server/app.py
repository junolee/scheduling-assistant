# coding: utf-8
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse
import numpy as np
import pandas as pd
import cPickle as pickle
from spacy.en import English
from sklearn.feature_extraction.text import CountVectorizer

#This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        msg = ' '.join(query_components["message"].split('%20'))
        reply = clf.predict([msg])[0]
        if reply == 'create_event':
            reply = 'Sure, I\'ll add that to the calendar!'
        else:
            reply = 'Let me check that for you.'
        self.wfile.write(reply)
    def log_message(self, format, *args):
        return

def tokenize(text): # get the tokens using spaCy
    tokens = parser(text)
    new = []
    for tok in tokens:
        new.append(tok.lemma_.lower().strip())
    tokens = new
    return tokens

if __name__ == '__main__':
    # unpickle model
    print 'unpickling model...'
    with open("models/classifier.pkl") as f:
        clf = pickle.load(f)
    print 'loading parser...'
    parser = English()

    try:
    	#Create a web server and define the handler to manage the
    	#incoming request
    	server = HTTPServer(('', 8080), myHandler)
    	print 'Python HTTP server started on port 8080!'

    	#Wait forever for incoming http requests
    	server.serve_forever()

    except KeyboardInterrupt:
    	print 'Shutting down the web server'
    	server.socket.close()
