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