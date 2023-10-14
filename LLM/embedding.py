import openai
import numpy as np
from config import ConfigParser

def get_embedding(content):
    text = content.replace("\n", " ")

    config = ConfigParser()
    embed_model_name = config.get(key='openai')['embedding_model']
    if embed_model_name in ["text-embedding-ada-002"]:
        openai.api_key = config.get(key='openai')['api_key']

        embedding_model = openai.Embedding
        embed = embedding_model.create(
            model = embed_model_name,
            input = [text]
        )

        embed = np.array(embed["data"][0]["embedding"])

    # else: # use other model from huggingface
    #     embed = embedding_model.encode([text], convert_to_tensor=True)
    # if len(embed.shape) == 1:
    #     embed = embed.unsqueeze(0).cpu().numpy()
    return embed