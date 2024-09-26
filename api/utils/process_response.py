from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def produce_response(patent, img_sum, indp_clm):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"This patent {patent}: ---{img_sum}---. This is the description of a system composition for a patent, compared to the independent claim: ---{indp_clm}---, could the patent {patent} be considered a prior art for the given claim?"}
        ]
    )
    final = response.choices[0].message.content
    return final