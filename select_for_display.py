import os
import json

with open("database.json", 'r') as f:
    data = json.load(f)

for company in data.keys():
    for year in data[company]:
        print(company, year)
        cleaned_path = os.path.join('cleaned', company, year + '.json')
        with open(cleaned_path, 'r') as f:
            cleaned_data = json.load(f)

        # government metrics
        for item in (filter(lambda x: x["topic"] == "G" and x["metric"], cleaned_data)):
            print(item)

        # government key points
        for item in (filter(lambda x: x["topic"] == "G" and not x["metric"], cleaned_data)):
            print(item)

        # social metrics
        for item in (filter(lambda x: x["topic"] == "S" and x["metric"], cleaned_data)):
            print(item)

        # social key points
        for item in (filter(lambda x: x["topic"] == "S" and not x["metric"], cleaned_data)):
            print(item)
        exit()
