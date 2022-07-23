"""
This script ingests each word list in categories/ into mongodb
Allow missing usage, origin, part
"""
import requests
import os
import json
from dotenv import load_dotenv
import os
import random
import sys
from time import sleep

load_dotenv()
OXFORD_APP_ID = os.getenv('OXFORD_APP_ID')
OXFORD_SECRET = os.getenv('OXFORD_SECRET')
TARGET_NUM_WORDS = 100

CATEGORIES_TO_SKIP = ['animals', 'astronomy']

# :param language <str> en-us or en-gb
def fetch_word(word, language='en-us'):
    try:
        print(word)
        fields = 'definitions,etymologies,pronunciations,examples'
        url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word + '?fields=' + fields;
        r = requests.get(url, headers = {'app_id': OXFORD_APP_ID, 'app_key': OXFORD_SECRET})
        if r.status_code == 404:
            print(f"{word} not found")
            return 404
        if r.status_code == 429:
            # HTTP 429 Too many requests
            print("API throttled...")
            sleep(5)
            return None
        if r.status_code != 200:
            print(f'Response {r.status_code}')
            return None
        response_data = r.json()
        # print(response_data)
        # take first lexicial entry
        data_first = response_data['results'][0]['lexicalEntries'][0]
        data = data_first['entries'][0]
        def_and_example = [d for d in data['senses'] if 'definitions' in d and 'examples' in d]
        usage = ""
        if def_and_example:
            def_and_example = def_and_example[0]
            usage = def_and_example['examples'][0]['text']
            # parse usage by surrounding word with brackets
            usage_lst = usage.split(" ")
            # print(usage_lst, word)
            i = usage_lst.index(word)
            usage_lst[i] = "[" + usage_lst[i] + "]"
            usage = " ".join(usage_lst)
        else:
            def_and_example = [d for d in data['senses'] if 'definitions' in d][0]
        pronunciation = [d for d in data['pronunciations'] if 'audioFile' in d][0]
        return {
            "word": word,
            "definition": def_and_example['definitions'][0],
            "usage": usage if usage else "",
            "origin": data['etymologies'][0] if 'etymologies' in data else "",
            "part": data_first['lexicalCategory']['id'],
            "audio": pronunciation['audioFile'],
            "phoneticNotation": pronunciation['phoneticNotation'],
            "phoneticSpelling": pronunciation['phoneticSpelling']
        }
    except Exception as e:
        _, _, exc_tb = sys.exc_info()
        print(f"WARNING failed to parse {word} with exception {e} line {exc_tb.tb_lineno}")
    return None

if __name__ == '__main__':
    categories_dir = os.path.join(os.getcwd(), 'categories')
    for category_file in os.listdir(categories_dir):
        category = category_file.split(".txt")[0]
        if category in CATEGORIES_TO_SKIP:
            continue
        print('Parsing category:', category)
        words_all = []
        with open(os.path.join(categories_dir, category_file), 'r') as f:
            for line in f:
                words_all.append(str(line.strip()))
        N = len(words_all)
        num_words = 0
        for i in random.sample(range(N), N):
            word = words_all[i]
            # skip plural words
            if word[-1] == 's':
                continue
            # US
            if num_words >= TARGET_NUM_WORDS:
                break
            data = fetch_word(word, 'en-us')
            if not data or data == 404:
                continue
            if data:
                num_words += 1
                print("GOT US WORD", data)
                with open(f'parsed_categories/{category}_us.txt', 'a', encoding="utf-8") as f:
                    f.write("%s\n" % data)
            # UK
            data = fetch_word(word, 'en-gb')
            if not data or data == 404:
                continue
            if data:
                print("GOT UK WORD", data)
                with open(f'parsed_categories/{category}_uk.txt', 'a', encoding="utf-8") as f:
                    f.write("%s\n" % data)