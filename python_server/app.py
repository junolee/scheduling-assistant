# coding: utf-8
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime, timedelta
from recurrent import RecurringEvent
from urlparse import urlparse
from spacy.en import English
import cPickle as pickle
import pandas as pd
import numpy as np
import dateutil
import random
# Google Calendar API
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

create_replies = ['Ok, just added that to your calendar!',
                  'Ok, scheduled that for you!']

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
        msg = '\''.join(msg.split('%27'))
        intent = clf.predict([msg])[0]
        if intent == 'create_event':
            r = RecurringEvent(now_date=datetime.now())
            dt = r.parse(msg)
            if "p.m." in msg and dt.hour < 12:
                dt += timedelta(hours=12)
            if "a.m." in msg and dt.hour > 12:
                dt -= timedelta(hours=12)
            reply = random.choice(create_replies)
            event = {
              'summary': 'Meeting',
              'start': {
                'dateTime': dt.isoformat(),
                'timeZone': 'America/Denver',
              },
              'end': {
                'dateTime': (dt + timedelta(hours=1)).isoformat(),
                'timeZone': 'America/Denver',
              }
            }
            event = service.events().insert(calendarId='primary', body=event).execute()

        else: #query_events
            now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            reply = 'Your Agenda:<br>'
            eventsResult = service.events().list(
                calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
                orderBy='startTime').execute()
            events = eventsResult.get('items', [])
            if not events:
                reply = 'No upcoming events found.'
            for event in events:
                start = event['start']
                if start.get('dateTime'):
                    dt = dateutil.parser.parse(start.get('dateTime'))
                    hour = str(dt.hour) if dt.hour <= 12 and dt.hour > 0 else str(abs(dt.hour-12))
                    minute = str(dt.minute) if dt.minute > 9 else '0' + str(dt.minute)
                    meridiem_indicator = ' AM' if dt.hour < 12 else ' PM'
                    date = dt.date()
                    time = hour + ':' + minute + meridiem_indicator
                else:
                    dt = dateutil.parser.parse(start.get('date'))
                    date = dt.date()
                    time = 'All-Day'
                reply += '<br>' + str(dt.month) + '/' + str(dt.day) + ' ' + time + ' ' + event['summary']
        self.wfile.write({"intent": intent, "reply": reply})
    def log_message(self, format, *args):
        return

def tokenize(text): # get the tokens using spaCy
    tokens = parser(text)
    new = []
    for tok in tokens:
        new.append(tok.lemma_.lower().strip())
    tokens = new
    return tokens

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

if __name__ == '__main__':
    print 'loading credentials and authorizing client...'
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

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
