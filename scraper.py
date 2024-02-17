import requests
from bs4 import BeautifulSoup
import os 
import re

import json

search_url = lambda x: f"https://www.responsibilityreports.com/Companies?search={x}"
make_url = lambda x: f"https://www.responsibilityreports.com{x}"

data = {}
if os.path.exists('database.json'):
    with open("database.json", 'r') as f:
        data = json.load(f)

def get_company_url(company):
    if not os.path.exists('data'):
        os.mkdir('data')

    response = requests.get(search_url(company))
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    first_company = soup.find('span', class_='companyName').find('a')
    company_name = first_company.text

    if company_name not in data:
        data[company_name] = []

    company_url = make_url(first_company['href'])
    response = requests.get(company_url)

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    parent_dir = f'data/{company_name}'
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)

    try:
        most_recent = soup.find('div', class_='most_recent_content_block').find('div', class_='view_btn').find('a')

        report_url = make_url(most_recent['href'])
        response = requests.get(report_url)
        file_name = f"{most_recent.text[:4]}.pdf"
        data[company_name].append(most_recent.text[:4])
        with open(os.path.join(parent_dir, file_name), 'wb') as f:
            f.write(response.content)
    except:
        print("Latest report failed.")    

    spans = soup.find_all('span', class_='btn_archived download')
    for span in spans:
        link = span.find('a')['href']
        response = requests.get(make_url(link))
        try:
            title = span.parent.find('span', class_="heading").text
            file_name = f"{str(title)[:4]}.pdf"
            data[company_name].append(str(title)[:4])
            with open(os.path.join(parent_dir, file_name), 'wb') as f:
                f.write(response.content)
        except:
            print("Older report failed.")

companies = ['nvidia', 'apple', 'microsoft', 'tesla']

for company in companies:
    get_company_url(company)

with open("database.json", 'w') as f:
    json.dump(data, f)
