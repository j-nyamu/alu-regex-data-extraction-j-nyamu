import json
import os

def save_output(data, filepath):
    # Error: Output folder might not exist, so we create it if needed
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Error: Something might go wrong while writing the file
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"\n✅ Results saved to {filepath}")

    except PermissionError:
        print(f"\n❌ Error: Permission denied — could not save to '{filepath}'.")
        print("  Try running the script as administrator or check folder permissions.")

    except Exception as e:
        print(f"\n❌ Unexpected error while saving output: {e}")