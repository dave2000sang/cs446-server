# Run this script to add/update difficulty for each word in US/UK word list

from utils import init_mongo, get_word_difficulty

def add_difficulty_to_word(words_cursor):
    for word in (words_cursor.find({}, {'word': 1})):
        word['difficulty'] = get_word_difficulty(word['word'])
        r = words_cursor.update_one({'word': word['word']}, {'$set': {'difficulty': word['difficulty']}})
        print(r)

if __name__ == '__main__':
    mongo = init_mongo()
    add_difficulty_to_word(mongo.spellingo.words_us)
    add_difficulty_to_word(mongo.spellingo.words_uk)