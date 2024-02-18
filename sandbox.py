import os
import json
from llm.monsterdeployment import generate_text as generate_text_monsterd
from llm.togetherai import generate_text as generate_text_togetherai

generate_text = generate_text_togetherai

with open("database.json", 'r') as f:
    data = json.load(f)

def generate_prompt(page_data):
    return """

""" + str(page_data) + "\nend``` \n ## Output\n"

for company in data.keys():
    for year in data[company]:
        print(company, year)
        cleaned_path = os.path.join('cleaned', company, year + '.json')
        with open(cleaned_path, 'r') as f:
            cleaned_data = json.load(f)

        # government metrics
        x = list(filter(lambda x: x["topic"] == "G" and x["metric"], cleaned_data))
        for item in x:
            print(item)
        # print(generate_text(generate_prompt(x)))

        # # government key points
        # for item in (filter(lambda x: x["topic"] == "G" and not x["metric"], cleaned_data)):
        #     print(item)

        # # social metrics
        # for item in (filter(lambda x: x["topic"] == "S" and x["metric"], cleaned_data)):
        #     print(item)

        # # social key points
        # for item in (filter(lambda x: x["topic"] == "S" and not x["metric"], cleaned_data)):
        #     print(item)

        # # environmental metrics
        # for item in (filter(lambda x: x["topic"] == "E" and x["metric"], cleaned_data)):
        #     print(item)

        # # environmental key points
        # for item in (filter(lambda x: x["topic"] == "E" and not x["metric"], cleaned_data)):
        #     print(item)
        exit()
