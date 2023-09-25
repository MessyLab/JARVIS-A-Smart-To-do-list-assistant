from .tables import ChatLog, Idea, Project, Task, Subtask

def update_project_db(session, project_id, new_name, new_description):
    project = session.query(Project).filter(Project.id == project_id).first()
    if project:
        project.name = new_name
        project.description = new_description
        session.commit()

def update_idea_db(session, idea_id, new_content):
    idea = session.query(Idea).filter(Idea.id == idea_id).first()
    if idea:
        idea.content = new_content
        session.commit()

# def update_idea