import ray
import subprocess
import io
import sys

@ray.remote
def execute_python(code):
    # Create a StringIO object to capture output
    output = io.StringIO()
    # Save the original stdout
    original_stdout = sys.stdout

    scope = {}
    try:
        # Redirect stdout to the StringIO object
        sys.stdout = output
        # Execute the provided code
        exec(code, scope)
    except Exception as e:
        # Capture any exceptions and add them to output
        output.write(f"Error: {e}")
    finally:
        # Reset stdout to its original state
        sys.stdout = original_stdout
    # Get all output as a single string
    return output.getvalue()