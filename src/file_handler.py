import os
import sys

def load_text(filepath):
    # Error: File not found
    if not os.path.exists(filepath):
        print(f"\nError: Input file '{filepath}' not found.")
        print("  Make sure 'raw-text.txt' exists inside the 'input/' folder.")
        sys.exit(1)

    with open(filepath, "r") as f:
        content = f.read()

    # Error: Empty file
    if not content.strip():
        print(f"\nError: Input file '{filepath}' is empty.")
        print("  Add some text to the file before running the script.")
        sys.exit(1)

    return content