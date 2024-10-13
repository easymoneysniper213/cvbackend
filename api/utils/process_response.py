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
            {
                "role": "system",
                "content": 
                    """
                    You task is to compare two different concepts for patents and determine whether A could be considered a prior art for B
                    For A, you will get: Patent ID, an independent claim for a patent, a list of system composition, a concept summary
                    For B, you will get: a list of system composition, a concept summary
                    Based on the information for each, complete the task. Compare and give a response in the structure:

                    - System Composition comparison
                        - ...
                        - ...
                        - ...
                    
                    - Concept Summary comparison
                        - ...
                        - ...
                        - ...
                    
                    - Conclusion
                        Based on the analysis from above, A could be considered a prior art or no A couldn't be considered a prior art

                    No other text other than this structure is needed
                    """
            },
            {
                "role": "user", 
                "content": 
                    f"""
                    A:
                    - Patent ID: {patent}
                    - Independent claim: {indp_clm}
                    - System Composition: {pat_sys_comp}
                    - Summary: {patent_sum}

                    B:
                    - System Composition: {pic_sys_comp}
                    - Summary: {pic_sum}
                    """
             }
        ]
    )
    final = response.choices[0].message.content
    return final