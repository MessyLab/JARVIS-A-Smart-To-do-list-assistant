import streamlit as st
from streamlit_chat import message
from database import Index
from init_databse import InitUtils
import openai
import function.function as F
from function import available_functions
import json
from prompt import format_response
from LLM import OpenAILLM
from utils import FunctionExcHelp


def main():
    init_utils = InitUtils()
    init_utils.init_streamlit()

    Session = init_utils.init_connection_db()
    indexdb = init_utils.init_connection_vb()
    
    st.title("JARVIS")
    query = st.chat_input("Enter your words")

    chat_model = OpenAILLM()

    if query:
        st.session_state["messages"].append({"role": "user", "content": query})

        first_respond = chat_model.get_response(messages=st.session_state['messages'],
                                                functions=F.function_list)

        st.session_state['past'].append(query)

        function_call = first_respond.get('function_call')

        if function_call:
            
            method_name, method_args = function_call.get('name'), function_call.get('arguments')

            # call function
            method_args_dict = json.loads(method_args)
            function_help = FunctionExcHelp(session=Session, 
                                            method_name=method_name, 
                                            method_args=method_args_dict,
                                            indexdb=indexdb
            )
            
            method_result = function_help.run()

            st.session_state['messages'].append(
                {"role": "user", "content": method_result}
            )

            second_response = chat_model.get_response(messages=st.session_state['messages'])
            print(second_response)

            st.session_state['generated'].append(second_response.get('content'))
            st.session_state['messages'].append(
                {"role": "assistant", "content": second_response.get('content')}
            )

        else:
            content = first_respond.get('content')
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