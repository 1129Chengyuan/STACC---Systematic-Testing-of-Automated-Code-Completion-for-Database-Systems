import csv
import datetime
import importlib
import os
from textwrap import indent
import argparse
import Azure_Code_Generator
import MasterTestCases
import re


def extract_code_segment(text):
    # Use regular expression to find the code segment between triple backticks
    match = re.search(r'```(.*?)```', text, re.DOTALL)

    if match:
        code_segment = match.group(1)
        # Remove the word "python" if present
        code_segment = code_segment.replace('python', '', 1).strip()
        return code_segment
    else:
        return ""


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
parser.add_argument('--model', type=str, default='gpt-4')
parser.add_argument('--increment', type=float, default=0.25)

parser.add_argument('--loop_var', type=str, default='temperature')
parser.add_argument('--loop_start', type=float, default=0)
parser.add_argument('--loop_end', type=float, default=2.0)

args = parser.parse_args()

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
setattr(args, var_name, args.loop_start)
header = ['Model',
          'Temperature',
          'Top_p',
          'Frequency_penalty',
          'Presence_penalty',
          'Code Generated',
          'Passed',
          'Error Report',
          "Execution Time for testcases (seconds)",
          "Memory Usage (KiB)"]

# Get the directory of the current script (__file__)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up two levels to get to the "STACC-V3" directory
project_dir = os.path.dirname(script_dir)
# Construct the results directory path (within the project directory)
results_dir = os.path.join(project_dir, "results")
results_dir = os.path.abspath(results_dir)
# Create a timestamped filename for the CSV file
now = datetime.datetime.now()
filename = now.strftime("%Y%m%d-%H%M%S") + ".csv"
filepath = os.path.join(results_dir, filename)

with open(filepath, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
    writer.writeheader()

while getattr(args, var_name) <= args.loop_end:
    # reset the CSVDataTable file
    with open('src/template.py', 'r') as firstfile, open('src/CSVDataTable.py', 'w') as secondfile:
        for line in firstfile:
            secondfile.write(line)
    code = Azure_Code_Generator.call_openai_api(
        prompt, args.temperature, max_tokens, args.top_p,
        args.frequency_penalty, args.presence_penalty,
        args.model, stop
    )
    code = extract_code_segment(code)
    code = indent(code, " " * 4)
    byte_code = code.encode('utf-8')
    print(code)
    with open('src/CSVDataTable.py', 'ab') as file:
        file.seek(0, 2)
        file.write(byte_code)
    if will_compile('src/CSVDataTable.py'):
        importlib.reload(module)
        results = MasterTestCases.get_test_report()
        row = {
            'Model': args.model,
            'Temperature': args.temperature,
            'Top_p': args.top_p,
            'Frequency_penalty': args.frequency_penalty,
            'Presence_penalty': args.presence_penalty,
            'Code Generated': code,
            'Passed': results['passed'],
            'Error Report': results,
            "Execution Time for testcases (seconds)": MasterTestCases.get_total_time(),
            "Memory Usage (KiB)": MasterTestCases.get_total_memory()
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
            'Code Generated': code,
            'Passed': results['passed'],
            'Error Report': results,
            "Execution Time for testcases (seconds)": 'NA',
            "Memory Usage (KiB)": 'NA'
        }
    row[var_name] = getattr(args, var_name)
    with open(filepath, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator='\n')
        writer.writerow(row)
    setattr(args, var_name, getattr(args, var_name) + args.increment)

# clear contents of CSVDataTable again
with open('src/CSVDataTable.py', 'w') as f:
    f.write('')
