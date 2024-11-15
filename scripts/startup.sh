#!/bin/bash

WORK_DIR=$HOME
cd $WORK_DIR

# Enable python virtual environment
cd python
source venv/bin/activate

# Run services
# Start Ray head node with the local IP address
ray start --head --node-ip-address=0.0.0.0 --port=8000

# Run the Flask application
python main.py