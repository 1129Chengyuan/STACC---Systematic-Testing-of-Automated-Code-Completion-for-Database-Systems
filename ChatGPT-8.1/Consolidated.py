import csv
import Azure_Code_Generator
import Code_Size_Checker
import MasterTestCases
from textwrap import indent
import importlib
import io


def will_compile(file_path):
    try:
        with open(file_path, 'r') as f:
            source = f.read()

        compile(source, file_path, mode='exec')
        return True

    except SyntaxError as err:
        print(f"Syntax error: {err}")
        return False


module = importlib.import_module("CSVDataTable")
# values to modify
data = []
# values
temperature = 0
max_tokens = 4096
top_p = 1
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

for i in range(9):
    data.append({})
    data[len(data) - 1]["Temperature"] = temperature
    data[len(data) - 1]["top_p"] = top_p
    data[len(data) - 1]["Frequency Penalty"] = frequency_penalty
    data[len(data) - 1]["Presence Penalty"] = presence_penalty
    data[len(data) - 1]["model"] = model
    # reset the CSVDataTable file
    with open('template.py', 'r') as firstfile, open('CSVDataTable.py', 'w') as secondfile:
        for line in firstfile:
            secondfile.write(line)
    code_generated = Azure_Code_Generator.call_openai_api(prompt, temperature, max_tokens, top_p, frequency_penalty,
                                                          presence_penalty, stop)
    code_generated = indent(code_generated, " " * 4)
    byte_code = code_generated.encode('utf-8')
    with open('CSVDataTable.py', 'ab') as file:
        file.seek(0, 2)
        file.write(byte_code)
    data[len(data) - 1]["Code Generated"] = code_generated
    with open('CSVDataTable.py', 'r') as f:
        print(f.read())
    if will_compile('CSVDataTable.py'):
        importlib.reload(module)
        test_case_result = MasterTestCases.get_test_report()
    else:
        test_case_result = {'total': 13, 'passed': 0, 'failed': 13, 'skipped': 0, 'errors': 13,
                            'failure_details': ["FAILED TO COMPILE"]}
    data[len(data) - 1]["Test Cases"] = test_case_result['passed']
    data[len(data) - 1]["Error Report"] = test_case_result
    # data[len(data) - 1].append(Code_Size_Checker.get_code_line(code_generated))
    # data[len(data) - 1].append(Code_Size_Checker.get_code_token(code_generated))
    data[len(data) - 1]["Execution Time for testcases (seconds)"] = MasterTestCases.get_total_time()
    data[len(data) - 1]["Memory Usage (KiB)"] = MasterTestCases.get_total_memory()
    temperature += 0.25

with open('data.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys(), lineterminator='')
    writer.writeheader()
    for row in data:
        writer.writerow(row)
# clear contents of CSVDataTable
with open('CSVDataTable.py', 'w') as f:
    f.write('')
