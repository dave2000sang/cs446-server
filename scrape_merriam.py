import requests
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


# find any 'vis' and returns it
def find_vis(d, parent):
    if not d:
        return ""
    if isinstance(d, str) and d == "vis":
        return parent[1][0]['t']
    if isinstance(d, list):
        for x in d:
            s = find_vis(x, d)
            if s:
                return s
    if isinstance(d, dict):
        for v in d.values():
            s = find_vis(v, d)
            if s:
                return s
    return ""


# param: d can be dict, list, or string
def get_first_ocurrence_of_key(d, k):
    if not d or d is str:
        return ""
    if isinstance(d, list):
        for x in d:
            s = get_first_ocurrence_of_key(x, k)
            if s:
                return s
    if isinstance(d, dict):
        if k in d:
            return d[k]
        for _, v in d.items():
            s = get_first_ocurrence_of_key(v, k)
            if s:
                return s
    return ""
    

def fetch_word(word):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}"
    res = requests.get(url, {"key": MERRIAM_KEY})
    try:
        response_data = res.json()
    except Exception as e:
        print("fuck", e)

    # take first one
    response_data = response_data[0]

    # parse common stuff
    shortdef = response_data['shortdef'][0]
    try:
        origin = response_data['et'][0][1]
    except KeyError:
        origin = ""
    if origin:
        origin = origin.replace("{it}", "").replace("{/it}", "")
    try:
        partofspeech = response_data['fl']
    except KeyError:
        partofspeech = ""
    audio = get_first_ocurrence_of_key(response_data['hwi']['prs'], "audio")
    if not audio:
        print("WARNING: didn't get audio")

    # find first correct 'sense'
    parsed = []
    usages = [find_vis(sense, None) for sense in response_data['def'][0]['sseq']]
    usages = [u for u in usages if u]
    usage = usages[0] if usages else ""
    # remove word from usage
    if usage:
        i = usage.find("{wi}")
        j = usage.find("{/wi}")
        usage = usage[:i] + "["+word+"]" + usage[j+5:]

    parsed.append({
        "word": word,
        "definition": shortdef,
        "usage": usage,
        "origin": origin,
        "part": partofspeech,
        "audio": audio,
    })
    return parsed[0] if parsed else parsed

if __name__ == '__main__':
    # Fetch data from API
    words_lst = [
        'adjust', 'alive', 'undertake', 'end', 'gossip', 'seal', 'penetrate', 'sheesh'
    ]
    data = [fetch_word(word) for word in words_lst]
    # send to mongo
    mongo = init_mongo()
    words = mongo.spellingo.words
    words.delete_many({'word': {'$in': words_lst}})
    result = words.insert_many(data)
    print(result.inserted_ids)
