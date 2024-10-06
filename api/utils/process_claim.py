from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def make_system_description(system_comp, pic):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"based on this claim for a patent: {pic}, and a given list of its system compositions: {system_comp}, give me a bullet point step by step description of how the system works. use * as bullet points. Give me this in just a paragraph, no other additional text is needed"}
        ]
    )
    final = response.choices[0].message.content
    return final

def make_img_description(system_comp, img_sum):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"based on this summary for a patent: {img_sum}, and a given list of its system compositions: {system_comp}, give me a bullet point step by step description of how the system works. use * as bullet points. Give me this in just a paragraph, no other additional text is needed"}
        ]
    )
    final = response.choices[0].message.content
    return final