import csv
import datetime
import importlib
import os
from textwrap import indent
import argparse
import Azure_Code_Generator
import MasterTestCases


def will_compile(file_path):
    try:
        with open(file_path, 'r') as read_file:
            source = read_file.read()

        compile(source, file_path, mode='exec')
        return True

    except SyntaxError as err:
        print(f"Syntax error: {err}")
        return False

parser = argparse.ArgumentParser()

parser.add_argument('--temperature', type=float, default=1)
parser.add_argument('--top_p', type=float, default=0.7)
parser.add_argument('--frequency_penalty', type=float, default=0)
parser.add_argument('--presence_penalty', type=float, default=0)
parser.add_argument('--model', type=str, default='chatgpt-4')
parser.add_argument('--increment', type=float, default=0.25)

parser.add_argument('--loop_var', type=str, default='temperature')
parser.add_argument('--loop_start', type=float, default=0)
parser.add_argument('--loop_end', type=float, default=2.0)

args = parser.parse_args()

# values to modify
data = []
# values
max_tokens = 4096
stop = None
prompt = """Generate a method called find_by_template that returns a record when given a dictionary template. 
            The structure is as follows:     
            def find_by_template(self, template, field_list=None):
                # :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}
                # :param field_list: A list of request fields of the form, ['fielda', 'fieldb', ...]                   
                # :return: A list containing dictionaries. A dictionary is in the list representing each record
                # that matches the template. The dictionary only contains the requested fields.
        """
module = importlib.import_module("CSVDataTable")

var_name = args.loop_var
var_value = getattr(args, var_name)

while var_value <= args.loop_end:
    # reset the CSVDataTable file
    with open('src/template.py', 'r') as firstfile, open('CSVDataTable.py', 'w') as secondfile:
        for line in firstfile:
            secondfile.write(line)
    code = Azure_Code_Generator.call_openai_api(
        prompt, args.temperature, max_tokens, args.top_p,
        args.frequency_penalty, args.presence_penalty,
        args.model, stop
    )
    code = indent(code, " " * 4)
    byte_code = code.encode('utf-8')
    with open('CSVDataTable.py', 'ab') as file:
        file.seek(0, 2)
        file.write(byte_code)
    with open('CSVDataTable.py', 'r') as f:
        print(f.read())
    if will_compile('CSVDataTable.py'):
        importlib.reload(module)
        results = MasterTestCases.get_test_report()
        row = {
            'Model':args.model,
            'Temperature':args.temperature,
            'Top_p':args.top_p,
            'Frequency_penalty':args.frequency_penalty,
            'Presence_penalty':args.presence_penalty,
            'Passed':results['passed'],
            'Error Report':results,
            "Execution Time for testcases (seconds)":MasterTestCases.get_total_time(),
            "Memory Usage (KiB)":MasterTestCases.get_total_memory()
        }
    else:
        results = {'total': 13, 'passed': 0, 'failed': 13, 'skipped': 0, 'errors': 13,
                            'failure_details': ["FAILED TO COMPILE"]}
        row = {
            'Model': args.model,
            'Temperature': args.temperature,
            'Top_p': args.top_p,
            'Freq_penalty': args.frequency_penalty,
            'Pres_penalty': args.presence_penalty,
            'Passed': results['passed'],
            'Error Report': results,
            "Execution Time for testcases (seconds)": 'NA',
            "Memory Usage (KiB)": 'NA'
        }
    row[var_name] = var_value
    data.append(row)
    var_value += args.increment
    setattr(args, var_name, var_value)

cwd = os.getcwd()
parent_dir = os.path.dirname(cwd)
# Build results folder path
results_dir = os.path.join(parent_dir, "results")

now = datetime.datetime.now()
filename = now.strftime("%Y%m%d-%H%M%S") + ".csv"
filepath = os.path.join(results_dir, filename)
# write to a new file
with open(filepath, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys(), lineterminator='')
    writer.writeheader()
    for row in data:
        writer.writerow(row)

# clear contents of CSVDataTable again
with open('CSVDataTable.py', 'w') as f:
    f.write('')
