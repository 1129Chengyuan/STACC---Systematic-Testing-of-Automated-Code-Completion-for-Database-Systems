import openai
import requests
import json
import os
import time

# Load environment variables from .env file
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# Configure OpenAI API
openai.api_type = 'azure'
openai.api_base = '' #add your own URL
openai.api_version = '' #add your API version
openai.api_key = ''  # Add your OpenAI API key here

def call_openai_api(prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, model, stop):
    retries = 3  # Number of times to retry on error

    for i in range(retries + 1):
        try:
            messages = [
                {"role": "system", "content": """Generate python code that works with CSV files when given a basic format and structure of a method. The constructor is as follows: 
                        class CSVDataTable(BaseDataTable):
                            def __init__(self, table_name, key_columns):
                                # :param table_name: Logical name of the table.
                                # :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
                                self.table_name = table_name
                                self.connect_info = connect_info
                                self.key_columns = key_columns
                    """},
                {"role": "user", "content": f"Give me the code and only the code for this: {prompt}"}
            ]

            # Set the headers
            headers = {
                "Content-Type": "application/json",
                "api-key": openai.api_key,  # Use the API key
                "Cache-Control": "no-cache"
            }

            # Set the payload
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "stop": stop
            }

            # Make the API call
            # MUST MODIFY! THIS CALL WILL DIFFER DEPENDING ON YOUR API VERSION!
            # EX: https://api.hku.hk/openai/deployments/{deployment-id}/chat/completions?api-version={api-version} from https://developer.hku.hk/api-details#api=azure-openai-service-api&operation=ChatCompletions_Create
            response = requests.post('https://api.hku.hk/openai/deployments/chatgpt/chat/completions?api-version=2023-03-15-preview', headers=headers, data=json.dumps(payload))

            message_content = response.json()["choices"][0]["message"]["content"]
            return message_content
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            if i < retries:
                print("Retrying...")
                time.sleep(40)
            else:
                raise  # If all retries failed, raise the exception

prompt = """Generate a method called find_by_template that returns a record when given a dictionary template. Assume there are no methods in the class. The structure is as follows:     
            def find_by_template(self, template, field_list=None):
                # :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}
                # :param field_list: A list of request fields of the form, ['fielda', 'fieldb', ...]                   
                # :return: A list containing dictionaries. A dictionary is in the list representing each record
                # that matches the template. The dictionary only contains the requested fields.
        """

