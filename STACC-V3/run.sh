#!/bin/bash

# Default values
TEMP=1
TOP_P=0.7
FREQ_PEN=0
PRES_PEN=0
MODEL="chatgpt"
INCR=0.25

LOOP_VAR="temperature"
LOOP_START=0
LOOP_END=2.0

# Read arguments
while getopts ":t:p:f:s:m:i:v:l:e" opt; do
  case $opt in
    t) TEMP=$OPTARG ;;
    p) TOP_P=$OPTARG ;;
    f) FREQ_PEN=$OPTARG ;;
    s) PRES_PEN=$OPTARG ;;
    m) MODEL=$OPTARG ;;
    i) INCR=$OPTARG ;;
    v) LOOP_VAR=$OPTARG ;;
    l) LOOP_START=$OPTARG ;;
    e) LOOP_END=$OPTARG ;;
  esac
done

# Run script
cd src
python -m main --temperature "$TEMP" \
               --top_p "$TOP_P" \
               --frequency_penalty "$FREQ_PEN" \
               --presence_penalty "$PRES_PEN" \
               --model "$MODEL" \
               --increment "$INCR" \
               --loop_var "$LOOP_VAR" \
               --loop_start "$LOOP_START" \
               --loop_end "$LOOP_END"

# Check results
if [ -f "../results/data.csv" ]; then
  echo "CSV generated"
else
  echo "Error generating CSV"
  exit 1
fi