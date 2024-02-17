from llm.togetherai import generate_output
import os
import json
import tqdm
import threading
import time

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
                result = generate_output(page)
                parse_data.append(result)
            except Exception as e:
                try:
                    time.sleep(1.1)
                    result0 = generate_output(page[:len(page)//2])
                    time.sleep(1.1)
                    result1 = generate_output(page[len(page)//2:])
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

