import json
import os

def save_output(data, filepath):
    # Create output folder if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"\n  Results saved to {filepath}")

    except PermissionError:
        print(f"\nError: Permission denied — could not save to '{filepath}'.")
        print("  Try running the script as administrator or check folder permissions.")

    except Exception as e:
        print(f"\nUnexpected error while saving output: {e}")