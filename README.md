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
1. Add oxford API credentials to `.env`
2. `python scrape_oxford.py`
3. `python upload_words.py`
