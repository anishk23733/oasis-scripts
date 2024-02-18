# Data Orchestration for Oasis at TreeHacks 2024

### Setup

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Create a `.env` file with your `TOGETHER_API_KEY` from https://www.together.ai/, `MONSTER_API_KEY` from https://monsterapi.ai/, and `PREDICTIONGUARD_TOKEN` from Intel Developer Cloud. If you are using a custom Monster Deployment, which we are, include the `MONSTER_DEPLOY_API_KEY` and `MONSTER_DEPLOY_URL` in the `.env` as well.


### Pipeline

First run `scraper.py` to build a `database.json` and pull documents.

Then run `cache_pdf.py` to pull text data from the scraped documents and cache them.

Then run `llm_page_parse.py` to run LLaMA 2 on these documents and extract key metrics for Oasis.

Then run `clean.py` to clean up the keyword data and save it in a more logical format.

Then run `populate_vectordb.py` to populate the vector db with embedded keyword data.

You can use the notebook `query_vectordb.ipynb` to inspect the data.

You can also use the notebook `rag.py` to converse with the agent and gain insights about a company's sustainability practices.


### Set up VectorDB

```
git clone git@github.com:alvin-isc/treehacks-2024.git intersystems
cd intersystems
docker run -d --name iris-comm -p 1972:1972 -p 52773:52773 intersystemsdc/iris-community:2024.1-preview
pip install -r requirements.txt

docker run -d -p 27017:27017 --name test-mongo mongo:latest
```

Follow other instructions at https://github.com/alvin-isc/treehacks-2024/blob/main/demo/langchain_demo.ipynb to get the IRIS password set up.
