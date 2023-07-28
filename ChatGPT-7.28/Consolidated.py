import csv
import Azure_Code_Generator
import Code_Size_Checker
from TestingGenCode.MasterTestCases import tests_success, get_total_time, get_total_memory

data = [["Temperature", "top_p", "frequency_penalty", "presence_penalty", "Model", "Code Generated",
         "Time Taken to Generate", "Correct testcases", "error report", "Code Size (lines)", "Code Size (tokens)",
         "Execution Time for testcases (seconds)", "Memory Usage (KiB)"]]
# values
temperature = 0.7
max_tokens = 4096
top_p = 0
frequency_penalty = 0
presence_penalty = 0
stop = None
model = "chatgpt-4"
prompt = """Generate a method called find_by_template that returns a record when given a dictionary template. The structure is as follows:     
            def find_by_template(self, template, field_list=None):
                # :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}
                # :param field_list: A list of request fields of the form, ['fielda', 'fieldb', ...]                   
                # :return: A list containing dictionaries. A dictionary is in the list representing each record
                # that matches the template. The dictionary only contains the requested fields.
        """


def return_gen_code():
    return data[len(data) - 1][5]


for i in range(5):
    data.append([])
    data[len(data) - 1].append((temperature, top_p, frequency_penalty, presence_penalty, model))
    code_generated = Azure_Code_Generator.call_openai_api(prompt, temperature, max_tokens, top_p, frequency_penalty,presence_penalty, stop)
    data[len(data) - 1].append(code_generated)
    print("code generation success")
    test_case_result = tests_success()
    data[len(data) - 1].append(test_case_result['passed'])
    data[len(data) - 1].append(test_case_result)
    data[len(data) - 1].append(Code_Size_Checker.get_code_line(code_generated))
    data[len(data) - 1].append(Code_Size_Checker.get_code_token(code_generated))
    data[len(data)-1].append(get_total_time())
    data[len(data)-1].append(get_total_memory())
    top_p += 0.25


with open('TestingGenCode/data.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='')
    writer.writerows(data)
