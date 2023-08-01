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

# code_sample = '''
# 12345
# '''
#
# code_size_token = get_code_token(code_sample)
# code_size_line = get_code_line(code_sample) - 2
# print(f"{code_size_line} lines")
# print(f"{code_size_token} tokens")
