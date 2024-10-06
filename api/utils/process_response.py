from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def produce_response(patent, pic_sum, patent_sum, pic_sys_comp, pat_sys_comp, indp_clm):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"""
             This patent {patent} has an independent claim {indp_clm}, and has system composition derived from this claim, 
             which is: {pat_sys_comp}. Based on this information {patent_sum} was created, i would like you to now analyze the 
             difference in summary and system composition before the patent mention above and my claim, which has a 
             system composition: {pic_sys_comp} and summary {pic_sum}. Analyze these two and if the patent {patent} covers
             all of the content mentioned in my summary and system composition, declare it could be a possible prior art.
             prior art being defined as: references or documents which may be used to determine novelty and/or non-obviousness of claimed subject matter in a patent application 
             Give me just the analysis and nothing else
             """}
        ]
    )
    final = response.choices[0].message.content
    return final