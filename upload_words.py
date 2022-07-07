import requests
import json
from dotenv import load_dotenv
import pymongo
import os
import random
import sys
from time import sleep


load_dotenv()
MONGO_PW = os.getenv('MONGO_PW')
MONGO_USER = os.getenv('MONGO_USER')
OXFORD_APP_ID = os.getenv('OXFORD_APP_ID')
OXFORD_SECRET = os.getenv('OXFORD_SECRET')

def init_mongo():
  # Replace the uri string with your MongoDB deployment's connection string.
  conn_str = f"mongodb+srv://{MONGO_USER}:{MONGO_PW}@spellingocluster.9o6km.mongodb.net/?retryWrites=true&w=majority"
  print(conn_str)
  client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=3000)
  try:
    client.server_info()
    print("Connected to mongo")
  except Exception as e:
      print("Unable to connect to mongo", e)
  return client


def ingest_into_mongo(lang):
    data = []
    with open(f"parsed_words_{lang}.txt", "r", encoding='utf-8') as f:
        for line in f:
            data.append(eval(line))
    words_lst = [d['word'] for d in data]
    # ingest words in mongo
    mongo = init_mongo()
    if lang == 'us':    
        words = mongo.spellingo.words_us
    else:    
        words = mongo.spellingo.words_uk
    words.delete_many({'word': {'$in': words_lst}})
    result = words.insert_many(data)
    print(result.inserted_ids)


if __name__ == '__main__':
    ingest_into_mongo('us')
    ingest_into_mongo('uk')
    