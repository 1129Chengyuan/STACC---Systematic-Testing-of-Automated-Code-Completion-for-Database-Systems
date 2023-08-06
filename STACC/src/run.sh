#!/bin/bash

# Script to run CSV generator Python code

# Default hyperparameters
TEMPERATURE=0.5
TOP_P=1.0
FREQ_PENALTY=0
PRES_PENALTY=0
MODEL="chatgpt-4"

# Read hyperparameters from arguments
while getopts ":t:p:f:s:m:" opt; do
  case $opt in
    t) TEMPERATURE="$OPTARG"
    ;;
    p) TOP_P="$OPTARG"
    ;;
    f) FREQ_PENALTY="$OPTARG"
    ;;
    s) PRES_PENALTY="$OPTARG"
    ;;
    m) MODEL="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
         exit 1
    ;;
  esac
done

# Run Python script
python3 main.py --temperature $TEMPERATURE \
                --top_p $TOP_P \
                --frequency_penalty $FREQ_PENALTY \
                --presence_penalty $PRES_PENALTY \
                --model $MODEL

# Check for generated CSV file
if [ -f "./data.csv" ]; then
  echo "CSV file generated successfully"
else
  echo "Error generating CSV file"
  exit 1
fi