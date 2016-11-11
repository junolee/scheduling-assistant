from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import string
import pandas as pd
import numpy as np
from spacy.en import English

def load_data():
    print 'loading data...'
    data = pd.read_csv('data/requests.csv').values
    print 'shuffling data...'
    np.random.shuffle(data)
    y = data[:,1]
    X = data[:,0]
    return X, y

# Every step in a pipeline needs to be a "transformer".
# Define a custom transformer to clean text using spaCy
class CleanTextTransformer(TransformerMixin):
    """
    Convert text to cleaned text
    """

    def transform(self, X, **transform_params):
        return [cleanText(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}

# A custom function to clean the text before sending it into the vectorizer
def cleanText(text):
    # lowercase
    text = text.lower()

    return text

# A custom function to tokenize the text using spaCy
# and convert to lemmas
def tokenizeText(sample):

    # get the tokens using spaCy
    tokens = parser(sample)

    # lemmatize
    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_)
    tokens = lemmas

    return tokens

def printNMostInformative(vectorizer, clf, N):
    """Prints features with the highest coefficient values, per class"""
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    topClass1 = coefs_with_fns[:N]
    topClass2 = coefs_with_fns[:-(N + 1):-1]
    print("Class 1 best: ")
    for feat in topClass1:
        print(feat)
    print("Class 2 best: ")
    for feat in topClass2:
        print(feat)

if __name__ == '__main__':
    parser = English()
    X, y = load_data()
    print 'splitting data...'
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    # the vectorizer and classifer to use
    # changed the tokenizer in CountVectorizer to use a custom function using spaCy's tokenizer
    vectorizer = CountVectorizer(tokenizer=tokenizeText, ngram_range=(1,1))
    clf = LinearSVC()
    # the pipeline to clean, tokenize, vectorize, and classify
    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer), ('clf', clf)])
    print 'fitting pipeline...'
    pipe.fit(X_train, y_train)
    print 'predicting values...'
    y_pred = pipe.predict(X_test)

    print("----------------------------------------------------------------------------------------------")
    print("results:")
    for (sample, pred) in zip(X_test, y_pred):
        print(sample, ":", pred)
    print("accuracy:", accuracy_score(y_test, y_pred))

    print("----------------------------------------------------------------------------------------------")
    print("Top 10 features used to predict: ")
    # show the top features
    printNMostInformative(vectorizer, clf, 10)

    print("----------------------------------------------------------------------------------------------")
    print("The original data as it appeared to the classifier after tokenizing, lemmatizing, stoplisting, etc")
    # let's see what the pipeline was transforming the data into
    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer)])
    transform = pipe.fit_transform(X_train, y_train)

    # get the features that the vectorizer learned (its vocabulary)
    vocab = vectorizer.get_feature_names()

    # the values from the vectorizer transformed data (each item is a row,column index with value as # times occuring in the sample, stored as a sparse matrix)
    for i in range(20):
        s = ""
        indexIntoVocab = transform.indices[transform.indptr[i]:transform.indptr[i+1]]
        numOccurences = transform.data[transform.indptr[i]:transform.indptr[i+1]]
        for idx, num in zip(indexIntoVocab, numOccurences):
            s += str((vocab[idx], num))
        print("Sample {}: {}".format(i, s))
