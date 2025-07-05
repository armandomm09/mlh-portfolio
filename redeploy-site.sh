#!/bin/bash

PROJECT_DIR="/root/mlh-portfolio"
START_SCRIPT="/root/start_server.sh"
TMUX_SESSION="flask_server"

echo "Starting redeployment process..."


echo "-> Stopping any existing tmux sessions..."
tmux kill-server || true
echo "Done."

echo "-> Navigating to project directory: $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "Error: Project directory not found. Aborting."; exit 1; }
echo "Done."

echo "-> Fetching the latest code from GitHub..."
git fetch origin
git reset --hard origin/main
echo "Done."

VENV_PATH=".venv/bin/activate"
if [ -f "$VENV_PATH" ]; then
    echo "-> Activating Python virtual environment..."
    source "$VENV_PATH"
    echo "Done."
    
    echo "-> Installing/updating Python dependencies..."
    pip install -r requirements.txt
    echo "Done."
else
    echo "Warning: Virtual environment not found at '$VENV_PATH'. Skipping dependency installation."
fi

echo "-> Starting new server in tmux session named '$TMUX_SESSION'..."
tmux new-session -d -s flask_server "/root/start_server.sh"

echo ""
echo "Redeployment complete!"
echo "Your site is now running in the background."
echo "You can check the server console with: tmux attach -t $TMUX_SESSION"
echo "To detach from the session (and leave it running), press: Ctrl+b, then d"