#!/bin/bash
#python3 demo-gen.py

# # Capture the exit code
# exit_code=$?

# # Check if it failed
# if [ $exit_code -ne 0 ]; then
#     echo "The Python code generation script failed with exit code $exit_code"
#     # Handle the failure case here...
# else
#     echo "The Python code generation script succeeded."
# fi

# Optionally, you could directly test and react without storing in a variable:
if ! python3 generate_crew.py; then
    echo "The Python script failed."
else
    python3 run_crew.py
fi

