from database import add_idea_db, get_ideas_db, update_idea_db, get_all_ideas_db, get_ideas_db_content
from .utils import preprocess_content
from prompt import format_response
import numpy as np

def search_idea(content_arr, index):
    scores, idxs = [[0]], [[-1]]
    if len(index) >= 1:
        scores, idxs = index.search(content_arr, 1)

    return scores, idxs

def add_idea(session, content, index):
    content_arr = preprocess_content(content)
    scores, idxs = search_idea(content_arr, index)
    print(scores, idxs)
    for i, score in enumerate(scores):
        if score[0] > 0.89:
            ideas = get_ideas_db(session, int(idxs[i]) + 1)
            res = [idea.content for idea in ideas]
            print("The res of search by sql")
            print(res)
            return format_response(res, 3)
        else:
            add_idea_db(session, content)
            index.add(content_arr)
            print("save a new idea")
            message = "I'll put the idea on the record, any other ideas"
            return format_response(message, 1)
        
def update_idea(session, previous_idea, new_idea, index):
    previous_arr = preprocess_content(previous_idea)
    scores, idxs = search_idea(previous_arr, index)
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
        update_idea_db(session, id, new_idea)
        
        print("Update the previous idea")
        message = "Well, I have change the previous idea"
        return format_response(message, 2)
    else:
        message = "There is no similar idea to update"
        return format_response(message, 2)

    
        
# def update_idea(session, content, index):
#     # where to get id and how to input it ?
#     content_arr = preprocess_content(content)
#     scores, idxs = search_idea(content_arr, index)
#     for i, score in enumerate(scores):
#         if score[0] > 0.9:
#             id = int(idxs[i] + 1)

#     try:
#         # update index
#         content_arr = preprocess_content(content)
#         index.update(id, content_arr)

#         print("finish updating the index")
#         # update idea db
#         update_idea_db(session, id, content)
        
#         print("Update the previous idea")
#         message = "Well, I have change the previous idea"
#         return format_response(message, 2)
#     except:
#         message = "There is no similar idea to update"
#         return format_response(message, 2)

def show_all_ideas(session, **kwargs):
    ideas = get_all_ideas_db(session)
    conts = [idea.content for i, idea in enumerate(ideas)]
    message = f"""{conts}"""
    return format_response(message, 4)