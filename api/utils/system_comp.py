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
            {
                "role": "system",
                "content": 
                    """
                    You will receive an independent claim from a patent. 
                    Based on this claim, create a system composition list, 
                    making sure to break the composition down into unique components
                    it should be in the following structure:
                    - ...
                    - ...
                    - ...
                    No other text other than this list is needed.
                    """
            },
            {
                "role": "user", 
                "content": query
            }
        ]
    )

    content_message = response.choices[0].message.content
    query_system_components = [
        re.sub(r'^[-\d)\.]+\s*', '', item.strip()) 
        for item in content_message.split("\n") if item.strip()
    ]

    return query_system_components
