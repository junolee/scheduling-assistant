import numpy as np
import pandas as pd
import cPickle as pickle
from spacy.en import English
from sklearn.feature_extraction.text import CountVectorizer

def tokenize(text): # get the tokens using spaCy
    tokens = parser(text)
    new = []
    for tok in tokens:
        new.append(tok.lemma_.lower().strip())
    tokens = new
    return tokens

if __name__ == "__main__":
    # unpickle model
    with open("models/classifier.pkl") as f:
        clf = pickle.load(f)
    print 'unpickled model!'
    print 'loading parser...'
    parser = English()
    print 'loaded parser!'
    # vectorizer = CountVectorizer(tokenizer=tokenize, ngram_range=(1,1))
    # print ' initialized vectorizer!'
    request = raw_input('Enter request: ')
    while request != 'quit':
        # x = vectorizer.fit_transform(request)
        y = clf.predict([request])
        print y
        request = raw_input('Enter request: ')
