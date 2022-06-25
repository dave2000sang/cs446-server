from flask import Flask, jsonify
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
    # for demo, just return any 10 words
    words = spellingo_db.words
    data = list(words.find({}, limit=10))
    for d in data:
        del d['_id']
    return jsonify(results = data)
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

# class Audio(Resource):
#     def get(self, word):
#         return {}

# api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
