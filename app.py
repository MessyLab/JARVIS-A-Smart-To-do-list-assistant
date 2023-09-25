import streamlit as st
from streamlit_chat import message
from database import Index
from init_databse import init_connection_db, init_connection_vb, init_streamlit
import openai
from database import add_chat_db
import function.function as F
from function.function_idea import add_idea, update_idea, show_all_ideas
from function.function_project import add_project, show_all_projects
from function.function_task import add_task, show_all_tasks
import json
from prompt import format_response

def main():
    init_streamlit()
    Session = init_connection_db()
    idea_index, proj_n_index, proj_d_index, task_index = init_connection_vb()
    
    st.title("Justin")

    openai.api_key = "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"

    query = st.chat_input("Enter your words")

    if query:
        st.session_state["messages"].append(
            {"role": "user", "content": query}
        )
        print(22222222)
        first_respond = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=st.session_state['messages'],
            functions=F.function_list,
            function_call="auto",
        )
        print(333333333)

        st.session_state['past'].append(query)
        function_call = first_respond.choices[0].message.get('function_call')

        if function_call:
            available_functions = {
                "add_idea": add_idea,
                "update_idea": update_idea,
                "show_all_ideas": show_all_ideas,
                "add_project": add_project,
                "add_task": add_task,
                "show_all_projects": show_all_projects,
                "show_all_tasks": show_all_tasks,
            }

            method_name, method_args = function_call.get('name'), function_call.get('arguments')

            # call function
            method_args_dict = json.loads(method_args)
            method_to_call = available_functions[method_name]
            print(method_name)
            if method_name == "show_all_ideas" or method_name == "show_all_projects":
                print(111111)
                method_result = method_to_call(session=Session)
            elif method_name == "add_idea":
                method_result = method_to_call(
                    session=Session,
                    content=method_args_dict["content"],
                    index=idea_index,
                )
            elif method_name == "update_idea":
                print(method_args_dict)
                method_result = method_to_call(
                    session=Session,
                    previous_idea=method_args_dict["previous_idea"],
                    new_idea=method_args_dict["new_idea"],
                    index=idea_index,
                )
            elif method_name == "add_project":
                method_result = method_to_call(
                    session=Session,
                    name=method_args_dict["name"],
                    description=method_args_dict["description"],
                    nindex=proj_n_index,
                    dindex=proj_d_index,
                )
            elif method_name == "add_task":
                print(method_args_dict)
                method_result = method_to_call(
                    session=Session,
                    project_name=method_args_dict["project_name"],
                    description=method_args_dict["description"],
                    tindex=task_index,
                    pnindex=proj_n_index,
                )
            elif method_name == "show_all_tasks":
                method_result = method_to_call(
                    session=Session,
                    project_name=method_args_dict["project_name"],
                    pnindex=proj_n_index,
                )

            st.session_state['messages'].append(
                {"role": "user", "content": method_result}
            )

            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=st.session_state['messages'],
            )

            st.session_state['generated'].append(second_response.choices[0].message.get('content'))
            st.session_state['messages'].append(
                {"role": "assistant", "content": second_response.choices[0].message.get('content')}
            )

        else:
            content = first_respond.choices[0].message.get('content')
            st.session_state['generated'].append(content)
            st.session_state['messages'].append(
                {"role": "assistant", "content": content}
            )

    response_container = st.container()

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

if __name__ == "__main__":
    main()