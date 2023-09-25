import faiss
from LLM.embedding import get_embedding
import numpy as np

def preprocess_content(content):
    content_arr = get_embedding(content)
    content_arr = content_arr[np.newaxis, :].astype(np.float32)
    faiss.normalize_L2(content_arr)
    return content_arr