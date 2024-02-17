from llm.togetherai import generate_text as generate_text_togetherai
from llm.intel import generate_text as generate_text_intel
from llm.monster import generate_text as generate_text_monster

import os
import json
import tqdm
import threading
import time

generate_text = generate_text_togetherai

def generate_prompt(page_data):
    return """
You are an analyst extracting key metrics and points from a page in an official document.\n
Note that you do not care about redundant information or irrelevant points.
You only extract key points that provide useful insights about a company's CSR.

The output should be a list of objects, where each object represents a single point or fact, and contains the following properties:

* value: The value of the point or fact, which can be a number, a metric, or a descriptive text.
* metric: A boolean indicating whether the value is a metric or not.
* topic: The topic of the point or fact, which can be "E" for environmental, "S" for social, or "G" for governance.
* description: A brief description of the point or fact, providing context and additional information.
* tags: An array of keywords or tags associated with the point or fact, which can be used for filtering or searching.

Do not include general statements. Only include points mentioning organizations, statistics, or proven action.
You respond with concise and accurate JSON formatted output, like as follows:\n
## Input\n
```start
[
    "Renewable electricity  Our retail stores, data centers, and offices  around the world currently source 100 percent  renewable electricity.",
    "Over 70 percent of companies on Apple\u2019s  Supplier List \u2014 those suppliers that make  up 98 percent of Apple\u2019s direct spend for  materials, manufacturing, and assembly of  our products worldwide \u2014 have committed to  100 percent renewable electricity.",
    "In addition,  many other smaller suppliers have also made these commitments.",
    "About 1.5  gigawatts of Apple-created renewable  electricity projects account for over 90 percent  of the renewable electricity our facilities use.",
    "In fiscal  year 2021, Apple avoided 180,000 metric tons  of CO 2e by shifting the mode of transport and  reducing product weight through the removal   of the power adapter from the box of  iPhone devices.",
    "And we\u2019ve expanded our relationship with Bureau of Energy Resources, initiating new government contracts.",
    "We also offer  our U.S. employees a transit subsidy of up to $100 per month, and at our Cupertino and surrounding Santa Clara Valley campus, we offer free coach buses to commute to and from our corporate offices.",
    "Apple has invested in the 2300-acre IP Radian Solar project in Brown County, Texas."
]
end```

## Output\n
```start
[
    {
        "value": "70 percent",
        "metric": true,
        "topic": "E",
        "description": "Percent of companies on Apple's Supplier List that have committed to 100 percent renewable electricity, making 98 percent of Apple's direct spend for materials, manufacturing, and assembly of products worldwide.",
        "tags": ["supplier", "renewable energy"]
    },
    {
        "value": "1.5 gigawatts",
        "metric": true,
        "topic": "E",
        "description": "Created from renewable energy projects that account for over 90 percent of the renewable electricity our facilities use.",
        "tags": ["renewable energy"]
    },
    {
        "value": "180,000 metric tons",
        "metric": true,
        "topic": "E",
        "description": "Metric tons of CO 2e avoided by shifting the mode of transport and reducing product weight through the removal of the power adapter from the box of iPhone devices.",
        "tags": ["carbon emissions"]
    },
    {
        "value": "$100",
        "metric": true,
        "topic": "S",
        "description": "Monthly transit subsidy for employees.",
        "tags": ["employee benefits"]
    },
    {
        "value": "Bureau of Energy Resources",
        "metric": false,
        "topic": "G",
        "description": "Expansion of relationship with Bureau of Energy Resources with new government contracts.",
        "tags": ["partnerships"]
    },
    {
        "value": "none",
        "metric": false,
        "topic": "S",
        "description": "Offer free coach buses to commute to and from corporate offices at Cupertino and surrounding the Santa Clara Valley campus.",
        "tags": ["employee benefits"]
    },
    {
        "value": "IP Radian Solar project",
        "metric": false,
        "topic": "E",
        "description": "Offer free coach buses to commute to and from corporate offices at Cupertino and surrounding the Santa Clara Valley campus.",
        "tags": ["renewable energy"]
    }
]
end```
Note that topic of the point or fact can only be "E", "S", or "G".

Provide analysis output for the following data, as a JSON list:\n
## Input\n
```start""" + str(page_data) + "end```## Output\n"

if not os.path.exists('parsed'):
    os.mkdir('parsed')

with open("database.json", 'r') as f:
    data = json.load(f)

for company in data.keys():
    for year in data[company]:
        print(company, year)
        path = os.path.join('text', company, year + '.json')
        parsed_path = os.path.join('parsed', company, year + '.json')

        if os.path.exists(parsed_path):
            continue

        parent_dir = os.path.join('parsed', company)
        
        parse_data = []
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)


        with open(path, 'r') as f:
            page_data = json.load(f)

        def threading_task(page):
            try:
                result = generate_text(generate_prompt(page))
                parse_data.append(result)
            except Exception as e:
                try:
                    time.sleep(1.1)
                    result0 = generate_text(generate_prompt(page[:len(page)//2]))
                    time.sleep(1.1)
                    result1 = generate_text(generate_prompt(page[len(page)//2:]))
                    parse_data.append([result0, result1])
                except Exception as e:
                    print(company, year, "failed", e)

        threads = []
        num_threads = 4
        for i in tqdm.tqdm(range(len(page_data['pages']) // num_threads)):
            for page in page_data['pages'][i*num_threads:i*num_threads+num_threads]:
                t = threading.Thread(target=threading_task, args=(page,))
                threads.append(t)
                t.start()
                time.sleep(1.1)
            for t in threads:
                t.join()

        with open(parsed_path, 'w') as f:
            json.dump({'parsed_pages': parse_data}, f)

