# cs446-server
Server for CS446 project

## Run flask server
```
export FLASK_APP=__init__.py
flask run
```
## API
GET /words
- Returns list of 10 words


## Useful scripts
To ingest new words into mongodb:

## How to Scrape words
1. Create a `.env` file in directory of cs446-server/ containing mongodb and oxford API credentials
2. `python scrape_oxford.py` - this randomly samples `words.txt` and appends words to `parsed_words_us.txt` and `parsed_words_uk.txt`
3. `python upload_words.py` - this ingests the words from `parsed_words_us.txt` and `parsed_words_uk.txt` into mongodb
