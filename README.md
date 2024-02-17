# Backend for the ___

### Setup

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Create a `.env` file with your `TOGETHER_API_KEY` from https://www.together.ai/ and `MONSTER_API_KEY` from https://monsterapi.ai/.

### Pipeline

First run `scraper.py` to build a `database.json` and pull documents. 
Then run `pdf.py` to pull text data from the scraped documents and cache them.
Then run `process_pages.py` to run LLaMA 2 on these documents and extract key metrics for Oasis.
Then run `clean.py` to clean up the keyword data and save it in a more logical format.