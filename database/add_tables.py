from .tables import ChatLog, Idea, Project, Task, Subtask, VectorDBRelated
# from ..LLM.embedding import get_embedding

class AddDB:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def add_chat_db(role, content, session):
        print("Add new message in the log")
        new_chat = ChatLog(role=role, content=content)
        session.add(new_chat)
        session.commit()
    
    @staticmethod
    def add_project_db(session, name, description):
        project = Project(name=name, description=description)
        session.add(project)
        session.commit()

    @staticmethod
    def add_task_db(session, project_id, description, project):
        task = Task(project_id=project_id, description=description, project=project)
        session.add(task)
        session.commit()

    @staticmethod
    def add_subtask_db(session, task_id, name, description):
        subtask = Subtask(task_id=task_id, name=name, description=description)
        session.add(subtask)
        session.commit()

    @staticmethod
    def add_idea_db(session, content):
        idea = Idea(content=content, related_project=None)
        session.add(idea)
        session.commit()

