from spacy.en import English
import pandas as pd
import numpy as np

def load_data():
    df = pd.read_csv("data/requests.csv")
    create_requests = df[df['type'] == 'create_event']['request']
    return list[create_requests]

def parse_text(corpus):
    docs = []
    for text in corpus:
        docs.append(parser(unicode(text)))
    return docs

def find_time(text):


def start_end_times(doc):
    '''return start and end times of an event based on a create_event request'''
    # If no time mentioned, return None values



if __name__ == '__main__':
    parser = English()
    data = load_data()
    docs = parse_text(data)
