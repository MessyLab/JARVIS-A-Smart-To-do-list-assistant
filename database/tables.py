from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Time, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime
import mysql

Base = declarative_base()

class ChatLog(Base):
    __tablename__ = 'chat_logs'
    chat_id = Column(Integer, primary_key=True)
    role = Column(Integer) # 0 system, 1 assistant, 2 user, 3 function
    content = Column(String(1000))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Idea(Base):
    __tablename__ = 'idea'
    id = Column(Integer, primary_key=True)
    content = Column(String(1000))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    related_project = Column(Integer, ForeignKey('projects.id'))

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String(1000))
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, default=None)
    status = Column(Integer, default=0) # 0 never start 1 working 2 down
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    # name = Column(String(200))
    description = Column(String(1000))
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, default=None)
    duration = Column(Time, default=None)
    status = Column(Integer, default=0) # 0 never start 1 working 2 down
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks")
    # subtasks = relationship("Subtask", back_populates="task")

class Subtask(Base):
    __tablename__ = 'subtasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String(1000))
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, default=None)
    duration = Column(Time, default=None)
    status = Column(Integer, default=0) # 0 never start 1 working 2 down
#     task_id = Column(Integer, ForeignKey('tasks.id'))
#     task = relationship("Task", back_populates="subtasks")

class VectorDBRelated(Base):
    __tablename__ = 'vectordbrelated'
    id = Column(Integer, primary_key = True)
    ttype = Column(Integer) # 0 project, 1 task, 2 subtask, 3 idea
    related_id = Column(Integer) 


def create_database(server, username, password, dbname):
    connection = mysql.connector.connect(
        host = server,
        user = username,
        password = password,
    )
    cursor = connection.cursor()
    cursor.execute(f"Create Database {dbname}")
    cursor.close()
    connection.close()

# def delete_project(session, project_id):
#     project = session.query(Project).filter(Project.id == project_id).first()
#     if project:
#         session.delete(project)
#         session.commit()