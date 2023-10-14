import faiss
import numpy as np
import os
import threading

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
    
class IndexDB:
    def __init__(self, idea_path, proj_n_path, proj_d_path, task_path):
        self.idea_path = idea_path
        self.proj_n_path = proj_n_path
        self.proj_d_path = proj_d_path
        self.task_path = task_path
        self.idea_index, self.proj_n_index, self.proj_d_index, self.task_index = None, None, None, None
        self.connection_vdb()

    def create_npdb(self, name):
        npdb = np.empty((0, 1536)).astype('float32')
        np.save(name, npdb)

    def __create_index_db(self):
        self.create_npdb(self.idea_path)
        self.create_npdb(self.proj_n_path)
        self.create_npdb(self.proj_d_path)
        self.create_npdb(self.task_path)
        print("Create the vector npy")

    def connection_vdb(self):
        if not os.path.isfile(self.idea_path):
            thread = threading.Thread(target=self.__create_index_db())
            thread.start()
            thread.join()
        self.idea_index = Index(self.idea_path)
        self.proj_n_index = Index(self.proj_n_path)
        self.proj_d_index = Index(self.proj_d_path)
        self.task_index = Index(self.task_path)