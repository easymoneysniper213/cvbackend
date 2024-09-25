import json
import os
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

embedding_function = OpenAIEmbeddings(
    model='text-embedding-ada-002',
    api_key=os.environ["OPENAI_API_KEY"]
)
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("cv-vectorbase")

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
            'metadata': match.get('metadata', {}) 
        }
        formatted_results.append(formatted_result)

    return formatted_results
