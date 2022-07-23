from xml.etree.ElementTree import QName
from dotenv import load_dotenv
import os
from utils import init_mongo

load_dotenv()
MONGO_PW = os.getenv('MONGO_PW')
MONGO_USER = os.getenv('MONGO_USER')
mongo = init_mongo()


def ingest_into_mongo():
    categories_dir = os.path.join(os.getcwd(), 'parsed_categories')
    for category_file in os.listdir(categories_dir):
        data = []
        category = category_file.split(".txt")[0]
        print("ingesting:", category)
        with open(os.path.join(categories_dir, f"{category}.txt"), "r", encoding='utf-8') as f:
            for line in f:
                data.append(eval(line))
        # this will create the collection if it doesn't exist
        category_collection = mongo.categories[category]
        words_lst = [d['word'] for d in data]
        # ingest words in mongo
        category_collection.delete_many({'word': {'$in': words_lst}})
        result = category_collection.insert_many(data)
        print(f"inserted {len(result.inserted_ids)} new words")
        if len(result.inserted_ids) > 0:
            category_no_locale = category.split("_")[0]
            mongo.categories.categories_list.update_one({'category': category_no_locale}, {'$set': {'category': category_no_locale}}, upsert=True)

if __name__ == '__main__':
    ingest_into_mongo()
    