from flask import Flask, jsonify, request
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

app = Flask(__name__)
# api = Api(app)
mongo = init_mongo()
spellingo_db = mongo.spellingo


@app.route("/words")
def words():
  limit = request.args.get('limit')
  if not limit:
    limit = 10
  else:
    limit = int(limit)
  locale = request.args.get('locale')
  if not locale:
    locale = 'us'
  # for demo, just return any 10 words
  if locale == 'us':
    words = spellingo_db.words_us
  else:
    words = spellingo_db.words_uk
  cursor = words.aggregate([{ "$sample": { "size": limit } } ])
  data = []
  for d in cursor:
    data.append(d)
  # data = list(words.find({}, limit=limit))
  for d in data:
    del d['_id']
  return jsonify(results = data)

if __name__ == '__main__':
    app.run(debug=True)
