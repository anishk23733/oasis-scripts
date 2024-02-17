import predictionguard as pg
from dotenv import load_dotenv
import json

load_dotenv()

def generate_text(prompt, system_prompt=""):
    response = pg.Completion.create(model="Llama-2-7B",
                            prompt=prompt, max_tokens=1024)

    return response['choices'][0]['text']
