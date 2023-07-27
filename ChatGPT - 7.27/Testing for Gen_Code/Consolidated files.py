import csv

data = [["Temperature", "top_p","frequency_penalty","presence_penalty","Model","Code Generated", "Time Taken to Generate","Correct testcases","% of correct testcases","Code Size (lines)","Code Size (tokens)","Execution Time for testcases (seconds)", "Memory Usage (KiB)" ]]

with open('data.csv', 'w') as f:
  writer = csv.writer(f, lineterminator='')
  writer.writerows(data)