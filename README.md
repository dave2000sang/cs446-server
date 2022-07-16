# cs446-server
Server for CS446 project

## Run flask server
```
export FLASK_APP=app.py
flask run
```
## API
GET /words
- Returns list of 10 words


## Useful scripts
To ingest new words into mongodb:

## How to Scrape words
1. Create an Oxford Dictionary API account at https://developer.oxforddictionaries.com/signup?plan_ids[]=2357356361005
2. Create a `.env` file in directory of cs446-server/ containing mongodb and oxford API credentials
    - Replace `OXFORD_APP_ID` and `OXFORD_SECRET` env variables with your Application ID and Application Key
3. `python scrape_oxford.py` - this randomly samples `words.txt` and appends words to `parsed_words_us.txt` and `parsed_words_uk.txt`
4. `python upload_words.py` - this ingests the words from `parsed_words_us.txt` and `parsed_words_uk.txt` into mongodb
