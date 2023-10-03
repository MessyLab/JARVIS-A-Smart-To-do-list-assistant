# system_prompt = """
#     你是一个项目与时间管理助手，你需要根据用户的输入，判断是项目，任务，子任务还是想法。并分别记录下来。
#     将项目，任务，子任务和想法记录下来，\
#     项目包括名称，描述，启动时间，项目，\
#     任务包括名称，描述，启动时间，项目持续时间，\
#     每个任务都是不同项目的子集，\
#     子任务包括名称，描述，启动时间，项目持续时间，\
#     每个子任务都是不同任务的子集， \
#     想法主要包括用户的感想，总结，思考，复盘等等，\
#     如果用户缺少上述信息的描述，需要询问用户补充，\
#     并询问用户是否完成项目或者想法的创建 \
#     如果用户确认或者进行到另外的对话当中，则调用函数保存项目或想法 \
# """

# system_prompt = """
#             你是一个想法和思考管理助手，你需要根据用户的提示，\
#             将想法记录下来，\
#             想法可能包括用户的感想，总结，思考，复盘等等，\
#             并询问用户是否完成项目或者想法的创建 \
#             如果用户确认或者进行到另外的对话当中，则调用函数保存项目或想法 \
#             """


system_prompt = """
            your name is Jusin \
            you are an idea and project manange assistant, you should save the user idea, project and task \
            An idea may be a thought, a summary, a reflection or a review \
            
            A project should include a name and a description \
            a task must has a description and a related project \
            
            You should ask the user if it have completed the creation of the idea or not \
            
            1. If user confirms it or moves on to another conversation, \
            the function is called to save the idea \
            
            2. If user new idea, project and task has same content with previous idea, project and task \
            Then ask user \
            to recheck the cotent and ask user to change the previous idea or not. \
            If user confirms to change the previous idea, then call the update idea function \
            to update the content. \

            3. If user want to get all the projects and ideas from the database, \
            return them
            """


def format_response(message:str, types:int):
    match types:
        case 1:
            dynamic_prompt = f"""
            Return the infomation to user some sentence similar like: 

            {message}
            
            Only return one sentence.
            """
            return dynamic_prompt
        case 2:
            freeze_prompt = f"""
            Return the following sentence without any change

            {message} 
            """
            return freeze_prompt
        case 3: # show all the idea, result is a list   RAG
            formated_prompt = f"""
            make the user input into delow format and return to user as a text style without code
            show all the content from user input  \

            user input {message} \

            n is the length of message. \

            Before and after the user input, you can say somthing like, \

            `I find the similar ideas, could you rechack them. If you \
            want to change them or do nothing, please let me know \
            `

            ```
            1. message[0] \
            ...       \
            n. message[n] \
            
            ```
            """
            return formated_prompt
        case 4: # show all the idea, the previous sentence is different
            formated_prompt = f"""
            Return all the ideas to the user.

            make the user input into delow format and return to user as a text style without code
            show all the content from user input  \

            user input {message} \

            n is the length of message. \

            Before and after the user input, you can say somthing like, \

            `I get all your ideas \
            `

            ```
            1. message[0] \
            ...       \
            n. message[n] \
            
            ```
            """
            return formated_prompt
        case 5: # show all the task, result is a list
            formated_prompt = f"""
            make the user input into delow format and return to user as a text style without code
            show all the content from user input  \

            user input {message} \

            n is the length of message. \

            Before and after the user input, you can say somthing like, \

            `I find the similar project, could you rechack them. If you \
            want to change them or do nothing, please let me know \
            `

            ```
            1. message[0][0]  message[0][1] \
            ...       \
            n. message[n][0]  message[n][1] \
            
            ```
            """
            return formated_prompt
        case 6: # show all the projects' name
            formated_prompt = f"""
            make the user input into delow format and return to user as a text style without code
            show all the content from user input  \

            user input {message} \

            n is the length of message. \

            Before and after the user input, you can say somthing like, \

            `I get all your projects \
            `

            ```
            1. message[0] \
            ...       \
            n. message[n] \
            
            ```
            """
            return formated_prompt