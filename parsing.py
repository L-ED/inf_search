from lxml import etree
import pymongo
from wikiextractor.extract import clean
import re
from torchtext.data import get_tokenizer
import json

def parse_corpus(data_path, vocabulary_path, dbname="corpus", colname="wikien"):

    title = None
    vocabulary = {}
    # first in doc goes title? after text
    # if textr is redirect, skip it and drop title
    doc_id = 0
    tknzr = get_tokenizer("basic_english")


    table = connect_to_database(dbname, colname)

    for _, element in etree.iterparse(data_path):
        
        tag = element.tag
        if tag.endswith('title'):
            title = element.tag
        elif tag.endswith('text'):
            text = element.text
            if text.startswith('#REDIRECT'):
                title=None
            else:
                text = clean_text(text)
                update_vocabulary(vocabulary, tknzr, text, doc_id)
                table.insert_one(
                    {'title':title, 'text':text, 'id':doc_id}
                )
                doc_id +=1

    save_vocabulary(vocabulary, vocabulary_path)
    

def connect_to_database(dbname, colname):

    client = pymongo.MongoClient("mongodb://localhost:27017/")

    try:
        client.admin.command("ismaster")
    except:
        print("This collection doesn't exist")

    mydb = client[dbname]
    mycol = mydb[colname]
    return mycol


def clean_text(text):

    text = clean(text)
    text = re.sub(u'[\n*=]+', '',text)
    return text


def update_vocabulary(voc, tokenizer, text, doc_id):

    for token in tokenizer(text):
        if token in voc:
            voc[token]['docs'].append(doc_id)
        else:
            voc[token]={'id':len(voc), 'docs':[doc_id]}


def save_vocabulary(voc, savepath):

    with open(savepath, 'w') as f:
        json.dump(voc, f)