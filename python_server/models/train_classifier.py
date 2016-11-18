import pandas as pd
import numpy as np
import cPickle as pickle
from spacy.en import English
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, precision_score

def load_data():
    data = pd.read_csv('~/dev/capstone/data/requests.csv').values
    np.random.shuffle(data)
    X = data[:,0]
    y = data[:,1]
    return X, y

def tokenize(text): # get the tokens using spaCy
    tokens = parser(text)
    new = []
    for tok in tokens:
        new.append(tok.lemma_.lower().strip())
    tokens = new
    return tokens

def score(model, X_test, y_test):
    score = model.score(X_test, y_test)
    return score

if __name__ == "__main__":
    parser = English()
    vectorizer = CountVectorizer(tokenizer=tokenize, ngram_range=(1,1))
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    rf = RandomForestClassifier(n_estimators=100)
    model = Pipeline([('vectorizer', vectorizer), ('rf', rf)])
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mat = confusion_matrix(y_test, y_pred)
    acc = score(model, X_test, y_test)

    print "Accuracy:", acc
    with open("classifier.pkl", 'w') as f:
        pickle.dump(model, f)
