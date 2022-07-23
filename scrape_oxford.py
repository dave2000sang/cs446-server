import requests
from dotenv import load_dotenv
import os
import random
import sys
from time import sleep, time
from utils import get_word_difficulty

load_dotenv()
OXFORD_APP_ID = os.getenv('OXFORD_APP_ID')
OXFORD_SECRET = os.getenv('OXFORD_SECRET')

TIMEOUT_AFTER_SECONDS = 1000
WORD_FILE = 'words.txt'
NUM_WORDS = 500

# :param language <str> en-us or en-gb
def fetch_word(word, language='en-us'):
    try:
        fields = 'definitions,etymologies,pronunciations,examples'
        strictMatch = 'true'
        url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word + '?fields=' + fields + '&strictMatch=' + strictMatch;
        r = requests.get(url, params={'fields': "definitions,etymologies,pronounciations"}, headers = {'app_id': OXFORD_APP_ID, 'app_key': OXFORD_SECRET})
        if r.status_code == 404:
            print(f"{word} not found")
            return 404
        if r.status_code == 429:
            # HTTP 429 Too many requests
            print("API throttled...")
            sleep(8)
            return None
        response_data = r.json()
        # print(response_data)
        # take first lexicial entry
        data_first = response_data['results'][0]['lexicalEntries'][0]
        data = data_first['entries'][0]
        def_and_example = [d for d in data['senses'] if 'definitions' in d and 'examples' in d][0]
        usage = def_and_example['examples'][0]['text']
        # parse usage by surrounding word with brackets
        usage_lst = usage.split(" ")
        # print(usage_lst, word)
        i = usage_lst.index(word)
        usage_lst[i] = "[" + usage_lst[i] + "]"
        usage = " ".join(usage_lst)

        pronunciation = [d for d in data['pronunciations'] if 'audioFile' in d][0]
        difficulty = get_word_difficulty(word)
        if not difficulty:
            print(f'skipping {word} too trivial')
            return None
        return {
            "word": word,
            "definition": def_and_example['definitions'][0],
            "usage": usage,
            "origin": data['etymologies'][0],
            "part": data_first['lexicalCategory']['id'],
            "audio": pronunciation['audioFile'],
            "phoneticNotation": pronunciation['phoneticNotation'],
            "phoneticSpelling": pronunciation['phoneticSpelling'],
            "difficulty": difficulty
        }
    except Exception as e:
        _, _, exc_tb = sys.exc_info()
        print(f"WARNING failed to parse {word} with exception {e} line {exc_tb.tb_lineno}")
    return None

if __name__ == '__main__':
    words_all = []
    with open(WORD_FILE, "r") as f:
        for line in f:
            words_all.append(str(line.strip()))
    N = len(words_all)
    # randomly sample US and UK words until have enough
    words_us = []
    words_uk = []

    t0 = time()
    for i in random.sample(range(N), N):
        if time() - t0 > TIMEOUT_AFTER_SECONDS:
            print("TIMEOUT")
            break
        word = words_all[i]
        # skip plural words
        if word[-1] == 's':
            continue
        sleep(0.5)
        # Fetch data from API
        if len(words_us) < NUM_WORDS:
            data = fetch_word(word, 'en-us')
            # skip bad words
            if not data or data == 404:
                continue
            if data:
                print("GOT US WORD", data)
                # write to file
                with open('parsed_words_us.txt', 'a', encoding="utf-8") as f:
                    f.write("%s\n" % data)
                words_us.append(data)
        if len(words_uk) < NUM_WORDS:
            data = fetch_word(word, 'en-gb')
            if data and data != 404:
                print("GOT UK WORD", data)
                # write to file
                with open('parsed_words_uk.txt', 'a', encoding="utf-8") as f:
                    f.write("%s\n" % data)
                words_uk.append(data)
        if len(words_uk) == NUM_WORDS and len(words_us) == NUM_WORDS:
            break

