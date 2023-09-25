import faiss
import numpy as np
import os

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class Index:
    def __init__(self, path):
        self.local_path = path
        self.npdb = np.load(self.local_path)

    def save(self):
        np.save(self.local_path, self.npdb)

    def add(self, arr):
        self.npdb = np.vstack([self.npdb, arr])
        self.save()

    def update(self, id, new_arr):
        self.npdb[id, :] = new_arr
        self.save()
        print("update id done")

    def search(self, arr, top_k):
        index = faiss.IndexFlatL2(1536)
        index.add(self.npdb)

        dist, idx = index.search(arr, top_k)
        score = 1 - dist / 2
        return score, idx
    
    def __len__(self):
        return self.npdb.shape[0]