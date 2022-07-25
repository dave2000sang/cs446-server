from utils import init_mongo

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
    