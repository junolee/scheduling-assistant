from flask import Flask, request, jsonify, url_for, redirect
import numpy as np
import pandas as pd
import pickle
import requests
from spacy.en import English

app = Flask(__name__)
PORT = 5000

parser = English()
def tokenize(text): # get the tokens using spaCy
    tokens = parser(text)
    new = []
    for tok in tokens:
        new.append(tok.lemma_.lower().strip())
    tokens = new
    return tokens

@app.route('/')
def index():
    return redirect(url_for('json_data'))

@app.route('/json-data/')
def json_data():
    # get number of items from the javascript request
    message = request.args.get('message', 'Did not receive message.')
    prediction = model.predict([message])[0]
    # return json
    print message
    return jsonify({'reply': prediction})

if __name__ == '__main__':

    with open("../models/classifier.pkl") as f:
        model = pickle.load(f)
    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
