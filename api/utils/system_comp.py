import os
from dotenv import load_dotenv
from openai import OpenAI
import re

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_system_composition(query):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"{query} The above is an independent claim from a patent, give me a list of the system composition based on the text, just the list nothing else"}
        ]
    )
    content_message = response.choices[0].message.content
    query_system_components = [
        re.sub(r'^\d+\.\s*', '', item.strip()) 
        for item in content_message.split("\n") if item.strip()
    ]
    return query_system_components