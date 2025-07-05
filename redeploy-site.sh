#!/bin/bash

PROJECT_DIR="~/mlh-portfolio"
TMUX_SESSION="flask_server"

echo "Starting redeployment "

PROJECT_DIR_EXPANDED=$(eval echo "$PROJECT_DIR")

echo "Stopping any existing tmux sessions..."
tmux kill-server || true
echo "Done."

cd "$PROJECT_DIR_EXPANDED" || { echo "Error: Project directory not found. Aborting."; exit 1; }

echo "Fetching the latest code from GitHub..."
git fetch origin
git reset --hard origin/main

VENV_PATH="venv/bin/activate"
if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    
    pip install -r requirements.txt
else
    echo "Warning: Virtual environment not found at '$VENV_PATH'. Skipping dependency installation."
    echo "The new server might fail to start."
fi

echo "Starting new server in tmux session named '$TMUX_SESSION'..."
tmux new -d -s "$TMUX_SESSION" "cd '$PROJECT_DIR_EXPANDED' && source '$VENV_PATH' && flask run --host=0.0.0.0"

echo ""
echo "Redeployment complete!"
echo "Your site is now running in the background."