from torchtext.data import get_tokenizer
from parsing import connect_to_database
import json
import numpy as np

def search(text_line, vocab_path, db_name, colname):

    collection = connect_to_database(db_name, colname)
    voc = load_vocabulary(vocab_path)

    # tknzr = get_tokenizer("basic_english")
    # tokens = tknzr(text_line)
    tokens = process_string(text_line)

    docs = take_tokens_docs(voc, tokens)
    intersected = find_intersections(docs)
    ask_for_doc(collection, intersected)


def process_string(line):

    words = line.split()
    bin_logic

    for i, word in enumerate(words):
        if word in bin_logic:
            edge_word = i in [0, i == len(words)-1]
            if i in [0, i == len(words)-1]: 
                raise ValueError('Binary logic should be between')
            else:

                any(word in bin_logic in [words[i+1], words[i-1]])




def load_vocabulary(path):

    with open(path, 'r') as f:
        voc = json.load(f)
    
    return voc


def take_tokens_docs(voc, tokens):


    for token in tokens:
        if token == 'NOT'


    return [
        voc[token]['docs'] for token in tokens
    ]


def find_intersections(documents_indexes):

