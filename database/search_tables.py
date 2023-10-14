from .tables import ChatLog, Idea, Project, Task, Subtask

class GetDB:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_all_chats_db(session):
        chats = session.query(ChatLog).all()
        session.close()
        return chats

    @staticmethod
    def get_all_projects_db(session):
        return session.query(Project).all()

    @staticmethod
    def get_project_db_id(session, idx):
        return session.query(Project).filter(Project.id == idx).all()

    @staticmethod
    def get_porject_db_obj_id(session, idx):
        return session.query(Project).filter(Project.id == idx).first()

    @staticmethod
    def get_project_db_name(session, name):
        return session.query(Project).filter(Project.name == name).all()

    @staticmethod
    def get_task_db(session, id=None, task_name=None, task_description=None):
        if id:
            return session.query(Task).filter(Task.id == id).all()
        elif task_name:
            return session.query(Task).filter(Task.name == task_name).all()
        elif task_description:
            return session.query(Task).filter(Task.description == task_description)
        else:
            print("Please input task name or task description")

    @staticmethod
    def get_subtask_db(session, subtask_name=None, subtask_description=None):
        if subtask_name:
            return session.query(Subtask).filter(Subtask.name == subtask_name)
        elif subtask_description:
            return session.query(Subtask).filter(Subtask.description == subtask_description)
        else:
            print("Please input subtask name or subtask description")
        
    @staticmethod
    def get_all_ideas_db(session):
        return session.query(Idea).all()

    @staticmethod
    def get_all_projects_db(session):
        return session.query(Project).all()

    @staticmethod
    def get_ideas_db(session, idx):
        return session.query(Idea).filter(Idea.id == idx).all()

    @staticmethod
    def get_ideas_db_content(session, content):
        return session.query(Idea).filter(Idea.content == content).all()

    @staticmethod
    def get_tasks_for_project_db(session, project_id):
        return session.query(Task).filter(Task.project_id == project_id).all()

    @staticmethod
    def get_subtasks_for_task_db(session, task_id):
        return session.query(Subtask).filter(Subtask.task_id == task_id).all()