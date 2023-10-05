import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import create_database, Base, IndexDB
import faiss
import os
from prompt.prompt import system_prompt
import numpy as np
import threading
from config import ConfigParser

class InitUtils:
    def __init__(self) -> None:
        self.config = ConfigParser()

    def init_connection_db(self):
        USERNAME = self.config.get(key='mysql_database')['user_name']
        PASSWORD = self.config.get(key='mysql_database')['password']
        SERVER = self.config.get(key='mysql_database')['server']
        DBNAME = self.config.get(key='mysql_database')['dbname']

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

    def init_connection_vb(self):
        index_dir = self.config.get(key='local_vector_database')['index_dir']
        idea_path = os.path.join(index_dir, self.config.get(key='local_vector_database')['idea_vdb_name'])
        proj_n_path = os.path.join(index_dir, self.config.get(key='local_vector_database')['project_name_vdb_name'])
        proj_d_path = os.path.join(index_dir, self.config.get(key='local_vector_database')['project_description_vdb_name'])
        task_path = os.path.join(index_dir, self.config.get(key='local_vector_database')['task_description_vdb_name'])
        indexdb = IndexDB(idea_path, proj_n_path, proj_d_path, task_path)
        return indexdb
        
    def init_streamlit(self):
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [{
                'role':'system', 
                'content': system_prompt,
                }] if system_prompt else ""
            