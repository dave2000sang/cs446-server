from turtle import update
from flask import Flask, jsonify, request
from datetime import datetime
from utils import init_mongo

# Store the word of the day in global variable that's updated at midnight
US_word_of_day = None
UK_word_of_day = None
word_of_day_date = datetime.min.date()   # date associated w/ word of the day

app = Flask(__name__)
# api = Api(app)
mongo = init_mongo()
spellingo_db = mongo.spellingo
categories_db = mongo.categories

def update_word_of_day():
  global US_word_of_day, UK_word_of_day, word_of_day_date
  # US
  while True:
    words = spellingo_db.words_us.aggregate([
      {"$sample": { "size": 1 } } 
    ])
    new_word = words.next()['word']
    if new_word != US_word_of_day:
      break
  US_word_of_day = new_word
  # UK
  while True:
    words = spellingo_db.words_uk.aggregate([
      {"$sample": { "size": 1 } } 
    ])
    new_word = words.next()['word']
    if new_word != US_word_of_day:
      break
  UK_word_of_day = new_word
  word_of_day_date = datetime.today().date()

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
  category = request.args.get('category')
  if not category:
    category = 'standard'
  difficulty = request.args.get('difficulty')
  if not difficulty:
    difficulty = 'medium'
  if category == 'standard':
    if locale == 'us':
      words = spellingo_db.words_us
    else:
      words = spellingo_db.words_uk
  else:
    # return categories
    if category in categories_db.list_collection_names():
      words = categories_db[category]
    else:
      return "Bad category", 400
  cursor = words.aggregate([
    {"$match": { "difficulty": difficulty }},
    {"$sample": { "size": limit } } 
  ])
  data = []
  for d in cursor:
    data.append(d)
  for d in data:
    del d['_id']
  return jsonify(results = data)

@app.route("/word_of_the_day")
def word_of_the_day():
  locale = request.args.get('locale')
  if not locale:
    locale = 'us'
  # see if need to update the word
  if datetime.today().date() > word_of_day_date:
    update_word_of_day()
  if locale == 'us':
    return jsonify(results = US_word_of_day)
  else:
    return jsonify(results = UK_word_of_day)


@app.route("/categories")
def categories():
  data = [c['category'] for c in categories_db.categories_list.find({})]
  return jsonify(results = data)
  
if __name__ == '__main__':
    app.run(debug=True)
