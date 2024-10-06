import json
import os
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
import math

load_dotenv()

embedding_function = OpenAIEmbeddings(
    model='text-embedding-ada-002',
    api_key=os.environ["OPENAI_API_KEY"]
)
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("cv-vectorbase")

def transform_score(score):
    new_score = 10 * (0.8 * score + 0.2 * score ** 3)
    return round(new_score, 2)

def retrieve_from_pinecone(query_system, top_k=20):
    new_query = " ".join(query_system)
    query_embedding = embedding_function.embed_query(new_query)
    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    formatted_results = []
    for match in result['matches']:
        formatted_result = {
            'id': match['id'],
            'metadata': match.get('metadata', {}),
            'score': transform_score(match['score'])
        }
        formatted_results.append(formatted_result)

    return formatted_results
