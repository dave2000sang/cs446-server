from utils import init_mongo

bad_words = []
with open('badwords.txt', 'r') as f:
    for word in f:
        bad_words.append(word.strip())
print(bad_words)

mongo = init_mongo()
print(mongo.spellingo.words_us.delete_many({'word': {'$in': bad_words}}))
print(mongo.spellingo.words_uk.delete_many({'word': {'$in': bad_words}}))