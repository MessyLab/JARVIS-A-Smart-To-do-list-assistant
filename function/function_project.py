from LLM.embedding import get_embedding
from database import add_db_function, get_db_function, update_db_fucntion
from .utils import preprocess_content
from prompt import format_response

class FunctionProj:
    def __init__(self) -> None:
        pass

    def search_project(self, ndesc_arr, index):
        scores, idxs = [[0]], [[-1]]
        print(len(index))
        if len(index) >= 1:
            scores, idxs = index.search(ndesc_arr, 1)

        return scores, idxs

    def add_project(self, session, name, description, nindex, dindex):
        name_arr = preprocess_content(name)
        des_arr = preprocess_content(description)
        # nscores, nidxs = search_project(name_arr, nindex)
        scores, idxs = self.search_project(des_arr, dindex)

        for i, score in enumerate(scores):
            if score[0] > 0.89:
                projects = get_db_function.get_project_db_id(session, int(idxs[i]) + 1)
                res = [(pro.name, pro.description) for pro in projects]
                return format_response(res, 3)
            else:
                add_db_function.add_project_db(session, name, description)
                nindex.add(name_arr)
                dindex.add(des_arr)
                print("save a project")
                message = "I'll put the project on the project list, any other project"
                return format_response(message, 1)
            
    def show_all_projects(self, session):
        """return all projects' name
        """
        projects = get_db_function.get_all_projects_db(session)
        names = [proj.name for proj in projects]
        print(names)
        message = f"""
                make the user input into delow format and return to user as a text style without code
                show all the content from user input  \

                user input {names} \

                n is the length of names. \

                Before and after the user input, you can say somthing like, \

                `I get all your projects \
                `

                ```
                1. names[0] \
                ...       \
                n. names[n] \
                
                ```
                """
        return message

    def search_project_name(self, session, name, nindex):
        name_arr = preprocess_content(name)
        scores, idxs = self.search_project(name_arr, nindex)

        for i, score in enumerate(scores):
            if score[0] > 0.9:
                projects = get_db_function.get_project_db_id(session, int(idxs[i]) + 1)
                res = [pro.id for pro in projects]
                return res[0]
        return -1

    def update_project(self, session, project_name, **kwargs):
        project_id = self.search_project_name(project_name)
        if project_id != -1:
            update_db_fucntion.update_project_db(session, project_id, **kwargs["values"])