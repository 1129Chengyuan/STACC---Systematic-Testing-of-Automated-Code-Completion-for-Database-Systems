import os
import datetime
import csv

# Get current working directory
cwd = os.getcwd()

# Go up 1 level
parent_dir = os.path.dirname(cwd)

# Build results folder path
results_dir = os.path.join(parent_dir, "results")

now = datetime.datetime.now()
filename = now.strftime("%Y%m%d-%H%M%S") + ".csv"

filepath = os.path.join(results_dir, filename)

with open(filepath, 'w') as f:
    writer = csv.writer(f)
    writer.writerow("test")
# write csv contents