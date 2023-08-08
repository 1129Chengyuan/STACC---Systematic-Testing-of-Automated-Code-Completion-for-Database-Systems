import os
import openai
import time

primary_key = ""
secondary_key = ""

openai.api_type = "azure"
openai.api_base = "https://api.hku.hk"
openai.api_version = "2023-03-15-preview"
openai.api_key = primary_key


def call_openai_api(prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, model, stop):
    retries = 3  # Number of times to retry on error

    for i in range(retries + 1):
        try:
            response = openai.ChatCompletion.create(
                engine=model,
                messages=[
                    {"role": "system", "content": """Assistant is used to generate python code that works with CSV files when given a basic format and structure of a method. The constructor is as follows: 
                        class CSVDataTable(BaseDataTable):
                            def __init__(self, table_name, connect_info, key_columns):
                                # :param table_name: Logical name of the table.
                                # :param connect_info: Dictionary of parameters necessary to connect to the data.
                                # :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
                                self.table_name = table_name
                                self.connect_info = connect_info
                                self.key_columns = key_columns
                    """},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop
            )
            # return response
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            if i < retries:
                print("Retrying...")
                time.sleep(40)
            else:
                raise  # If all retries failed, raise the exception


prompt = """Generate a method called find_by_template that returns a record when given a dictionary template. The structure is as follows:     
            def find_by_template(self, template, field_list=None):
                # :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}
                # :param field_list: A list of request fields of the form, ['fielda', 'fieldb', ...]                   
                # :return: A list containing dictionaries. A dictionary is in the list representing each record
                # that matches the template. The dictionary only contains the requested fields.
        """
temperature = 0.7
max_tokens = 4096
top_p = 0
frequency_penalty = 0
presence_penalty = 0
stop = None


