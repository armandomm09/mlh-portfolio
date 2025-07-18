#!/bin/bash

PROJECT_DIR=$(eval echo ~/mlh-portfolio)
VENV_PATH=".venv/bin/activate"


echo "Changing directory to $PROJECT_DIR"
cd "$PROJECT_DIR" || exit 1
source "$VENV_PATH"

echo "Starting Flask server using: $FLASK_EXEC"
flask run --host=0.0.0.0