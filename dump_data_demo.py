from dotenv import load_dotenv
import pymongo
import os

load_dotenv()
MONGO_PW = os.getenv('MONGO_PW')
MONGO_USER = os.getenv('MONGO_USER')
MERRIAM_KEY = os.getenv('MERRIAM_KEY')

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

def read_data():
  import csv
  reader = csv.DictReader(open('demo_data.csv'))
  data = []
  for row in reader:
    print(row)
    data.append({k.strip(): v.strip() for k, v in row.items()})
  return data

if __name__ == '__main__':
  mongo = init_mongo()
  spellingo_db = mongo.spellingo
  words = spellingo_db.words

  data = read_data()
  print(data)
  result = words.insert_many(data)
  print(result.inserted_ids)