from abc import abstractclassmethod
import openai
import os
import time
from memory import *
from config import ConfigParser
from prompt import system_prompt, format_response

class LLM:
    def __init__(self) -> None:
        pass

    @abstractclassmethod
    def get_response():
        pass


class OpenAILLM(LLM):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.config = ConfigParser()

        self.API_KEY = self.config.get(key='openai')['api_key']
        self.PROXY = self.config.get(key='openai')['proxy']
        self.model = self.config.get(key='openai')['chat_model']
        self.temperature = self.config.get(key='openai')['temperature']
        
    def get_response(self,
                     messages,
                     stream=False,
                     functions=None,
                     function_call="auto",
                     **kwargs):
        openai.api_key = self.API_KEY
        if self.PROXY:
            openai.proxy = self.PROXY
        model = self.model
        temperature = self.temperature

        while True:
            try:
                if functions:
                    response = openai.ChatCompletion.create(
                        model = model,
                        messages = messages,
                        functions = functions,
                        function_call = function_call,
                        temperature = temperature,
                    )
                else:
                    response = openai.ChatCompletion.create(
                        model = model,
                        messages = messages,
                        temperature = temperature,
                        stream = stream,
                    )
                break
            except Exception as e:
                print(e)

        return response.choices[0].message
