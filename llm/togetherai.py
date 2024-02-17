from langchain_together import Together
import os
from dotenv import load_dotenv

load_dotenv()

llm = Together(
    # model="deepseek-ai/deepseek-coder-33b-instruct",
    model="meta-llama/Llama-2-70b-chat-hf",
    temperature=0.7,
    max_tokens=1028,
    top_k=1,
)

def generate_text(prompt, system_prompt=""):
    return llm.invoke(system_prompt + '\n' + prompt)