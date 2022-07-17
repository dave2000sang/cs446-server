from flask import Flask, jsonify, request
from datetime import datetime
from utils import init_mongo

app = Flask(__name__)
# api = Api(app)
mongo = init_mongo()
spellingo_db = mongo.spellingo
categories_db = mongo.categories

date_fmt = '%Y-%m-%d'
default_word_of_day = {'us_word': '', 'uk_word': '', 'date': datetime.min.date().strftime(date_fmt)}

def update_word_of_day(old_word_of_day):
  us_word = old_word_of_day['us_word']
  uk_word = old_word_of_day['uk_word']
  # US
  while True:
    words = spellingo_db.words_us.aggregate([
      {"$sample": { "size": 1 } } 
    ])
    new_word = words.next()
    if new_word['word'] != us_word:
      break
  us_word = new_word
  # UK
  while True:
    words = spellingo_db.words_uk.aggregate([
      {"$sample": { "size": 1 } } 
    ])
    new_word = words.next()
    if new_word['word'] != uk_word:
      break
  uk_word = new_word
  return {
      'us_word': us_word,
      'uk_word': uk_word,
      'date': datetime.today().date().strftime(date_fmt),
    }

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
  if category == 'standard':
    if locale == 'us':
      words = spellingo_db.words_us
    else:
      words = spellingo_db.words_uk
    if difficulty:
      cursor = words.aggregate([
        {"$match": { "difficulty": difficulty }},
        {"$sample": { "size": limit } } 
      ])
    else:
      cursor = words.aggregate([
        {"$sample": { "size": limit } } 
      ])

  else:
    # return categories
    if category in categories_db.list_collection_names():
      words = categories_db[category]
    else:
      return "Bad category", 400
    # don't filter difficulty if category specified
    cursor = words.aggregate([
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
  if len(list(mongo.spellingo.word_of_day.find({}))) == 0:
    mongo.spellingo.word_of_day.insert_one(default_word_of_day)
  word_of_day_entry = list(mongo.spellingo.word_of_day.find({}))[0]
  old_date = datetime.strptime(word_of_day_entry['date'], date_fmt)
  # see if need to update the word
  if datetime.today().date() > old_date.date():
    updated_word_of_day = update_word_of_day(word_of_day_entry)
    r = mongo.spellingo.word_of_day.update_one({}, {'$set': updated_word_of_day}, upsert=False)
    print("updated word of day. result=", r)
  if locale == 'us':
    del word_of_day_entry['us_word']['_id']
    return jsonify(results = word_of_day_entry['us_word'])
  else:
    del word_of_day_entry['uk_word']['_id']
    return jsonify(results = word_of_day_entry['uk_word'])


@app.route("/categories")
def categories():
  data = [c['category'] for c in categories_db.categories_list.find({})]
  return jsonify(results = data)
  
if __name__ == '__main__':
    app.run(debug=True)
