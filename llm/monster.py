import requests
import time

import os
from dotenv import load_dotenv

load_dotenv()

MONSTER_API_KEY = os.getenv('MONSTER_API_KEY')
url = "https://api.monsterapi.ai/v1/generate/llama2-7b-chat"


def make_request(prompt, system_prompt=""):
    payload = {
        "system_prompt": system_prompt,
        "prompt": prompt,
        "beam_size": 1,
        "max_length": 1024,
        "repetition_penalty": 1.2,
        "temp": 0.98,
        "top_k": 40,
        "top_p": 0.9
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {MONSTER_API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)
    process_id = response.json().get('process_id')
    return process_id

def check_status(process_id):
    url = f"https://api.monsterapi.ai/v1/status/{process_id}"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {MONSTER_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def generate_text(prompt, system_prompt=""):
    process_id = make_request(prompt, system_prompt)
    status = check_status(process_id)
    while status.get('status') != "COMPLETED":
        status = check_status(process_id)
        time.sleep(0.1)
    result = status.get('result').get('text')
    return result