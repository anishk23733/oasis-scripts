from PyPDF2 import PdfReader
import os
import json
import spacy
import re

nlp = spacy.load("en_core_web_sm")

if not os.path.exists('text'):
    os.mkdir('text')

def get_pdf_text(pdf_doc):
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text = page.extract_text()
        yield text

with open("database.json", 'r') as f:
    data = json.load(f)

def check_coherence(sentence):
    has_subject = False
    has_verb = False
    for token in sentence:
        if "subj" in token.dep_:
            has_subject = True
        if "VERB" == token.pos_:
            has_verb = True
    # If any sentence lacks a subject or a verb, return False
    if not (has_subject and has_verb):
        return False
    # If all sentences seem coherent, return True
    return True

for company in data.keys():
    for item in data[company]:
        print(company, item)
        path = os.path.join('data', company, item + '.pdf')

        json_path = item + '.json'
        parent_dir = os.path.join('text', company)
        
        # This report has already been parsed
        if os.path.exists(os.path.join(parent_dir, json_path)):
            continue

        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)

        page_data = {
            'pages': []
        }

        for page in get_pdf_text(path):
            text = re.sub(r'\n+', ' ', page)
            doc = nlp(text)
            
            sentences = []
            for sentence in doc.sents:
                if check_coherence(sentence):
                    sentences.append(str(sentence))
            if sentences:
                page_data['pages'].append(sentences)

        with open(os.path.join(parent_dir, json_path), 'w') as f:
            json.dump(page_data, f)
