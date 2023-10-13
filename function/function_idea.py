from database import add_db_function, get_db_function, update_db_fucntion
from .utils import preprocess_content
from prompt import format_response
import numpy as np

class FunctionIdea:
    def __init__(self) -> None:
        pass

    def __search_idea(self, content_arr, index):
        scores, idxs = [[0]], [[-1]]
        if len(index) >= 1:
            scores, idxs = index.search(content_arr, 1)

        return scores, idxs

    def add_idea(self, session, indexdb, method_args_dict):
        content = method_args_dict["content"]
        index = indexdb.idea_index
        content_arr = preprocess_content(content)
        scores, idxs = self.__search_idea(content_arr, index)
        print(scores, idxs)
        for i, score in enumerate(scores):
            if score[0] > 0.89:
                ideas = get_db_function.get_ideas_db(session, int(idxs[i]) + 1)
                res = [idea.content for idea in ideas]
                print("The res of search by sql")
                print(res)
                return format_response(res, 3)
            else:
                add_db_function.add_idea_db(session, content)
                index.add(content_arr)
                print("save a new idea")
                message = "I'll put the idea on the record, any other ideas"
                return format_response(message, 1)
            
       
    def update_idea(self, session, indexdb, method_args_dict ):
        previous_idea = method_args_dict["previous_idea"]
        new_idea = method_args_dict["new_idea"]
        index = self.indexdb.idea_index,
        
        previous_arr = preprocess_content(previous_idea)
        scores, idxs = self.__search_idea(previous_arr, index)
        print(scores)
        print(idxs)
        id = -1
        for i, score in enumerate(scores):
            if score[0] > 0.89:
                id = int(idxs[i] + 1)
        
        print(id)
        if id != -1:
            # update index
            content_arr = preprocess_content(new_idea)
            index.update(id - 1, content_arr)

            print("finish updating the index")
            # update idea db
            update_db_fucntion.update_idea_db(session, id, new_idea)
            
            print("Update the previous idea")
            message = "Well, I have change the previous idea"
            return format_response(message, 2)
        else:
            message = "There is no similar idea to update"
            return format_response(message, 2)

    def show_all_ideas(self, session, indexdb, method_args_dict):
        ideas = get_db_function.get_all_ideas_db(session)
        conts = [idea.content for i, idea in enumerate(ideas)]
        message = f"""{conts}"""
        return format_response(message, 4)