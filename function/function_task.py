from LLM.embedding import get_embedding
from database import add_task_db, get_task_db, get_project_db_id, get_porject_db_obj_id, get_tasks_for_project_db, update_task_db
from .utils import preprocess_content
from prompt import format_response
from .function_project import search_project, search_project_name

def search_task(ndesc_arr, index):
    scores, idxs = [[0]], [[-1]]
    print(len(index))
    if len(index) >= 1:
        scores, idxs = index.search(ndesc_arr, 1)

    return scores, idxs

def add_task(session, description, project_name, tindex, pnindex):
    ndesc_arr = preprocess_content(description)
    scores, idxs = search_task(ndesc_arr, tindex)
    for i, score in enumerate(scores):
        if score[0] > 0.89:
            tasks = get_task_db(session, id=int(idxs[i]) + 1)
            res = [task.description for task in tasks]
            return format_response(res, 3)

        else:
            project_id = search_project_name(session, project_name, pnindex)
            project = get_porject_db_obj_id(session, project_id)
            if project_id != -1:
                print()
                add_task_db(session, project_id=project_id, description=description, project=project)
                tindex.add(ndesc_arr)
                print("save a task")
                message = "I'll put the task in the task list, any other task"
                return format_response(message, 1)
    message = "I can not get the project"
    return format_response(message, 1)

def show_all_tasks(session, project_name, pnindex):
    project_id = search_project_name(session, project_name, pnindex)
    project = get_porject_db_obj_id(session, project_id)
    if project:
        name = project.name
        tasks = get_tasks_for_project_db(session, project_id)
        tasks_mes = []
        for task in tasks:
            if task.status == 0:
                tasks_mes.append((task.description, "never start"))
            elif task.status == 1:
                tasks_mes.append((task.description, "Working"))
            else:
                tasks_mes.append((task.description, "Done"))
        message = f"""
                make the user input into delow format and return to user as a text style without code
                show all the content from user input  \

                user input {tasks_mes} \

                n is the length of message. \

                Before and after the user input, you can say somthing like, \

                `All the task related to project $${name}$$ \
                `

                ```
                1. tasks_mes[0][0], the status of the task is tasks_mes[0][1] \
                ...       \
                n. tasks_mes[n][0], the status of the task is tasks_mes[n][1] \
                
                ```
                """
        return message
    else:
        return "Sorry I can not find the project what you want"

def update_task(session, description, project_name, tindex, pnindex, **kwargs):
    task_desc_arr = preprocess_content(description)
    project_id = search_project_name(session, project_name, pnindex)
    print("project id", project_id)
    task_id = search_task(task_desc_arr, tindex)[1][0]
    print("task id", task_id)
    update_task_db(session, int(task_id[0] + 1), project_id, **kwargs['values'])
    return "update the task"
