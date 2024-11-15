import ray

# Define a simple task
@ray.remote
def example_task(data):
    result = data ** 2
    return result