from dotenv import load_dotenv
import pymongo
import os
from wordfreq import zipf_frequency
from math import log

load_dotenv()
MONGO_PW = os.getenv('MONGO_PW')
MONGO_USER = os.getenv('MONGO_USER')

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

def get_word_difficulty(word):
  """
  Get difficulty for this word
  Define word difficulty as a combination of its frequency and length
  :param word: str
  :returns str of 'easy', 'medium', or 'hard', None is returned for trivial words and should be dropped
  """
  freq = zipf_frequency(word, 'en', 'best') # this returns in range [0, 8] higher = more frequent
  difficulty = 8 - freq + log(len(word))
  if difficulty <= 2:
    return None
  elif difficulty <= 4:
    return 'easy'
  elif difficulty <= 7:
    return 'medium'
  else:
    return 'hard'