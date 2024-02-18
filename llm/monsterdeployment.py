import os
from dotenv import load_dotenv
from monsterapi import client as mclient
import json

load_dotenv()

api_key = os.environ["MONSTER_DEPLOY_API_KEY"]
deploy_client = mclient(api_key = api_key)
url = os.environ["MONSTER_DEPLOY_URL"]
service_client  = mclient(api_key = api_key, base_url = url)

def generate_text(prompt, system_prompt=""):

    payload = {
        "input_variables": {"system": system_prompt,
            "prompt": prompt},
        "stream": False,
        "temperature": 0.6,
        "max_tokens": 1024
    }

    output = service_client.generate(model = "deploy-llm", data = payload)

    return json.loads(output)['text'][0]