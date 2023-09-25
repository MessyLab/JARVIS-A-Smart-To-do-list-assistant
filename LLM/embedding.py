import openai
import numpy as np

def get_embedding(content):
    test = content.replace("\n", " ")
    content_embeddings = openai.Embedding.create(
        input = [content],
        engine = "text-embedding-ada-002"
    )
    return np.array(content_embeddings['data'][0]['embedding'])