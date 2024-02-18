import os
from dotenv import load_dotenv
import json
import time
import tqdm

load_dotenv()

from langchain.docstore.document import Document
from langchain_together import TogetherEmbeddings
from langchain_iris import IRISVector
from sqlalchemy.exc import OperationalError

from langchain.embeddings import HuggingFaceEmbeddings

# embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-2k-retrieval")
embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

username = 'SUPERUSER'
password = 'oasis' # Replace password with password you set 
# http://localhost:52773/csp/sys/UtilHome.csp
# change from 'SYS'
hostname = 'localhost' 
port = '1972' 
namespace = 'USER'
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"
COLLECTION_NAME = "vectordb"

db = IRISVector(
    embedding_function=embeddings,
    dimension=768,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)

db.delete_collection()
db.create_collection()

with open("database.json", 'r') as f:
    data = json.load(f)

for company in data.keys():
    for year in data[company]:
        print(company, year)
        cleaned_path = os.path.join('cleaned', company, year + '.json')

        with open(cleaned_path, 'r') as f:
            cleaned_data = json.load(f)

        docs = []

        for entry in tqdm.tqdm(cleaned_data):
            entry['year'] = year
            entry['company'] = company

            docs.append(Document(page_content=entry["description"], metadata=entry))
            if len(docs) > 20:
                uploaded = False
                while not uploaded:
                    try:
                        db.add_documents(docs)
                        uploaded = True
                    except (OperationalError):
                        time.sleep(2)
                docs = []
        
        uploaded = False
        while not uploaded:
            try:
                db.add_documents(docs)
                uploaded = True
            except (OperationalError):
                time.sleep(2)
        time.sleep(.1)
        # break