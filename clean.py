import os
import json
import tqdm

if not os.path.exists('cleaned'):
    os.mkdir('cleaned')

with open("database.json", 'r') as f:
    data = json.load(f)

def find_substring(full_string, start_marker, end_marker):
    # Find the start of the desired substring
    start_index = full_string.find(start_marker)
    if start_index == -1:
        return None  # Start marker not found
    
    # Adjust start_index to get the actual beginning of the substring
    start_index += len(start_marker)
    
    # Find the end of the desired substring
    end_index = full_string.find(end_marker, start_index)
    if end_index == -1:
        return None  # End marker not found
    
    # Extract and return the substring
    return full_string[start_index:end_index]

for company in data.keys():
    for year in data[company]:
        print(company, year)
        path = os.path.join('parsed', company, year + '.json')
        cleaned_path = os.path.join('cleaned', company, year + '.json')

        if os.path.exists(cleaned_path):
            continue

        parent_dir = os.path.join('cleaned', company)
        
        parse_data = []
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)

        with open(path, 'r') as f:
            llm_data = json.load(f)
        i = 0

        for page in llm_data['parsed_pages']:
            if type(page) == list:
                combined = []
                for sub_page in page:
                    sub_page = find_substring(sub_page, '```start', 'end```')
                    try:
                        parsed = json.loads(sub_page)
                        for val in parsed:
                            val["id"] = f"{year}.{i}"
                            i += 1
                        combined += parsed
                    except:
                        pass
                parse_data += combined
            else:
                sub_page = find_substring(page, '```start', 'end```')
                try:
                    parsed = json.loads(sub_page)
                    for val in parsed:
                        val["id"] = f"{year}.{i}"
                        i += 1
                    parse_data += parsed
                except:
                    pass
        
        with open(cleaned_path, 'w') as f:
            json.dump(parse_data, f)
