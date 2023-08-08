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
print('''
#!/bin/bash\n\n# Default values\nTEMP=1\nTOP_P=0.7\nFREQ_PEN=0\nPRES_PEN=0\nMODEL="chatgpt-4"\nINCR=0.25\n\nLOOP_VAR="temperature"\nLOOP_START=0\nLOOP_END=2.0\n\n# Read arguments\nwhile getopts ":t:p:f:s:m:i:v:s:e" opt; do\n  case $opt in\n    t) TEMP=$OPTARG ;;\n    p) TOP_P=$OPTARG ;;\n    f) FREQ_PEN=$OPTARG ;;\n    s) PRES_PEN=$OPTARG ;;\n    m) MODEL=$OPTARG ;;\n    i) INCR=$OPTARG ;;\n    v) LOOP_VAR=$OPTARG ;;\n    l) LOOP_START=$OPTARG ;;\n    e) LOOP_END=$OPTARG ;;\n  esac\ndone\n\n# Run script\ncd src\npython -m main --temperature "$TEMP" \\\n               --top_p "$TOP_P" \\\n               --frequency_penalty "$FREQ_PEN" \\\n               --presence_penalty "$PRES_PEN" \\\n               --model "$MODEL" \\\n               --increment "$INCR" \\\n               --loop_var "$LOOP_VAR" \\\n               --loop_start "$LOOP_START" \\\n               --loop_end "$LOOP_END"\n\n# Check results\nif [ -f "../results/data.csv" ]; then\n  echo "CSV generated"\nelse\n  echo "Error generating CSV"\n  exit 1\nfi'
''')