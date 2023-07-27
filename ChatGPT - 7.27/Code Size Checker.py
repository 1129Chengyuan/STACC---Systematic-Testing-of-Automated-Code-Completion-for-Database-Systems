import sys
import tokenize
import io
def get_code_token(code):
    tokens = tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline)
    size = len(list(tokens))
    return size
def get_code_line(code):
    lines = code.split('\n')
    size = len(lines)
    return size

code_sample = '''
    def find_by_template(self, template, field_list=None):
        if not template:
            raise ValueError("Template cannot be empty.")

    results = []

    with open(self.table_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if all(row[k] == v for k, v in template.items()):
                
                if field_list == "*" or field_list is None:
                    result = row  
                
                elif field_list is not None:
                    result = {}
                    for field in field_list:
                        if field in row:
                            result[field] = row[field]
                        else:
                            raise KeyError(f"Requested field_list member '{field}'"\
                                            " does not exist in target data.")
       
                 results.append(dict(result))]
                  
    return results
'''

code_size_token = get_code_token(code_sample)
code_size_line = get_code_line(code_sample) - 2
print(f"{code_size_line} lines")
print(f"{code_size_token} tokens")
