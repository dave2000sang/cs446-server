# Run this script to add/update difficulty for each word in US/UK word list

from utils import init_mongo, get_word_difficulty

def add_difficulty_to_word(words_cursor):
    for word in (words_cursor.find({}, {'word': 1})):
        word['difficulty'] = get_word_difficulty(word['word'])
        if not word['difficulty']:
            print(f'deleting {word} trivial')
            r = words_cursor.delete_one({'word': word['word']})
            print(r)
        r = words_cursor.update_one({'word': word['word']}, {'$set': {'difficulty': word['difficulty']}})
        print(r)

if __name__ == '__main__':
    mongo = init_mongo()
    add_difficulty_to_word(mongo.spellingo.words_us)
    add_difficulty_to_word(mongo.spellingo.words_uk)

    # get distribution by difficulty
    easy = list(mongo.spellingo.words_us.find({'difficulty': 'easy'}))
    medium = list(mongo.spellingo.words_us.find({'difficulty': 'medium'}))
    hard = list(mongo.spellingo.words_us.find({'difficulty': 'hard'}))

    print('num words:', len(easy) + len(medium) + len(hard))

    print(f"num easy: {len(easy)} - {[word['word'] for word in easy]}")
    print(f"num medium: {len(medium)} - {[word['word'] for word in medium]}")
    print(f"num hard: {len(hard)} - {[word['word'] for word in hard]}")
    
