import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import create_database, Base, add_chat_db, Index
import faiss
import os
from prompt.prompt import system_prompt
import numpy as np
import threading

@st.cache_resource
def init_connection_db():
    USERNAME = "root"
    PASSWORD = ""
    SERVER = "127.0.0.1"
    DBNAME = "justin"

    DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{SERVER}:3306/{DBNAME}"

    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
    except:
        create_database(SERVER, USERNAME, PASSWORD, DBNAME)
        engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    Session = session()
    return Session

# def create_index(name):
#     index = faiss.IndexFlatL2(1536)
#     content_arrs = np.empty((0, 1536)).astype('float32')
#     index.add(content_arrs)
#     faiss.write_index(index, name)
def create_npdb(name):
    npdb = np.empty((0, 1536)).astype('float32')
    np.save(name, npdb)

def create_index_db():
    idea_path = "index_db/ideas_test.npy"
    create_npdb(idea_path)
    pro_n_path = "index_db/project_name_test.npy"
    pro_d_path = "index_db/project_des_test.npy"
    create_npdb(pro_n_path)
    create_npdb(pro_d_path)
    task_path = "index_db/task_test.npy"
    create_npdb(task_path)
    print("Create the vector npy")

def init_connection_vb():
    idea_path = "index_db/ideas_test.npy"
    pro_n_path = "index_db/project_name_test.npy"
    pro_d_path = "index_db/project_des_test.npy"
    task_path = "index_db/task_test.npy"
    if not os.path.isfile(idea_path):
        thread = threading.Thread(target=create_index_db)
        thread.start()
        thread.join()
    idea_index = Index(idea_path)
    pro_n_index = Index(pro_n_path)
    pro_b_index = Index(pro_d_path)
    task_index = Index(task_path)
    return idea_index, pro_n_index, pro_b_index, task_index
    
def init_streamlit():
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{
            'role':'system', 
            'content': system_prompt
            }]