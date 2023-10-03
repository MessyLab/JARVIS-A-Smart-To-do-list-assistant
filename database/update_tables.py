from .tables import ChatLog, Idea, Project, Task, Subtask

def update_project_db(session, project_id, **kwargs):
    project = session.query(Project).filter(Project.id == project_id).first()
    if project:
        project.name = kwargs["name"] if "name" in kwargs and kwargs["name"] != project.name else project.name
        project.description = kwargs["description"] if "description" in kwargs else project.description
        project.start_time = kwargs["start_time"] if "start_time" in kwargs else project.start_time
        project.end_time = kwargs["end_time"] if "end_time" in kwargs else project.end_time
        project.status = int(kwargs["status"]) if "status" in kwargs else project.status
        session.commit()
    else:
        return "Can not find the project"

def update_idea_db(session, idea_id, new_content):
    idea = session.query(Idea).filter(Idea.id == idea_id).first()
    if idea:
        idea.content = new_content
        session.commit()

def update_task_db(session, task_id, project_id, **kwargs):
    task = session.query(Task).filter(Task.id == task_id).first()

    if task:
        task.description = kwargs["description"] if "description" in kwargs else task.description
        task.start_time = kwargs["start_time"] if "start_time" in kwargs else task.start_time
        task.end_time = kwargs["end_time"] if "end_time" in kwargs else task.end_time
        task.status = int(kwargs["status"]) if "status" in kwargs else task.status
        task.duration = kwargs["duration"] if "duration" in kwargs else task.duration
        task.project_id = kwargs["project_id"] if "project_id" in kwargs else task.project_id
        session.commit()
    else:
        return "Can not find the task"