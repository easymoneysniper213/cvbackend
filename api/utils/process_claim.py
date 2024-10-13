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
            {
                "role": "system", 
                "content": 
                    """
                    You will be provided a claim for a patent, as well as a list of its system composition, 
                    based on these two, provide a bullet point step by step system works
                    The bullet point list should look like the following:
                    * ...
                    * ...
                    * ...
                    No other text other than this list is needed
                    """
            },
            {
                "role": "user", 
                "content": 
                    f"""
                    Claim: {pic} 
                    System Compositions: {system_comp}
                    """
            }
        ]
    )
    final = response.choices[0].message.content
    return final

def make_img_description(system_comp, img_sum):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": 
                    """
                    You will be provided an image summary of a diagram for a patent, as well as a list of its system composition, 
                    based on these two, provide a bullet point step by step system works
                    The bullet point list should look like the following:
                    * ...
                    * ...
                    * ...
                    No other text other than this list is needed
                    """
            },
            {
                "role": "user", 
                "content": 
                    f"""
                    Summary : {img_sum}
                    System Compositions: {system_comp}
                    """
            }
        ]
    )
    final = response.choices[0].message.content
    return final