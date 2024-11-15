from flask import Flask, request, jsonify
import time
import ray

# Import tasks
from tasks.examples import example_task
from tasks.python_execution import execute_python

app = Flask(__name__)

# Define the /check-health
@app.route('/check-health')
def check_health():
    try:
        return jsonify({"status": "Health OK"}), 200
    except Exception as e:
        return jsonify({"status": "Health Not OK"}), 400

# Route to trigger a task
@app.route('/trigger-task', methods=['POST'])
def trigger_task():
    print("Start task -Example Task")

    data = request.json.get("data")
    if data is None:
        return jsonify({"error": "No data provided"}), 400

    # Submit the task to Ray
    try:
        task_result = example_task.remote(data)
        result = ray.get(task_result)

        print("End task - Example Task")

        return jsonify({
            "status": "Task completed",
            "result": result
        }), 200
    except Exception as e:
        print("Error in task - Example Task")
        return jsonify({"error": str(e)}), 500

# Route to execute Python code
@app.route('/execute-python', methods=['POST'])
def execute_python_task():
    print("Start task - Execute Python Task")

    code = request.json.get("code")
    if code is None:
        return jsonify({"error": "No code provided"}), 400

    # Submit the code execution task to Ray
    try:
        start_time = time.time()
        task_result = execute_python.remote(code)
        processing_time = time.time() - start_time
        result = ray.get(task_result)

        print("End task - Execute Python Task")

        return jsonify({
            "status": "Task completed",
            "result": result,
            "processingTime": processing_time
        }), 200
    except Exception as e:
        print("Error in task - Execute Python Task")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000)
