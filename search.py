from parsing import connect_to_database
import json
import numpy as np
from string_parser import get_parser


def search(text_line, vocab_path, db_name, colname):

    collection = connect_to_database(db_name, colname)
    voc = load_vocabulary(vocab_path)

    parser, lexer = get_parser()
    docs_boolmask = parser(
        text_line, lexer).calc_ids(voc)
    
    ask_for_doc(
        collection, 
        np.where(docs_boolmask)[0].tolist()
    )


def load_vocabulary(path):

    with open(path, 'r') as f:
        voc = json.load(f)
    
    return voc


def ask_for_doc(collection, indexes):

    for elem in collection.find({'id':{'$in':indexes}}): 
        print(elem.title)
