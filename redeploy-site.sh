#!/bin/bash

PROJECT_DIR="/root/mlh-portfolio"
START_SCRIPT="/root/start_server.sh"

echo "Starting redeployment process..."


echo "-> Stopping portfolio service"
systemctl stop myportfolio
echo "Done."

cd "$PROJECT_DIR" || { echo "Error: Project directory not found. Aborting."; exit 1; }
echo "Done."

echo "Fetching the latest code from GitHub..."
git fetch origin
git reset --hard origin/main
echo "Done."

VENV_PATH=".venv/bin/activate"
if [ -f "$VENV_PATH" ]; then
    echo "-> Activating Python virtual environment..."
    source "$VENV_PATH"
    echo "Done."

    echo "Updating Python dependencies..."
    pip install -r requirements.txt
    echo "Done."
else
    echo "Warning: Virtual environment not found at '$VENV_PATH'. Skipping dependency installation."
fi

echo "Restarting portfolio service"
systemctl start myportfolio

echo ""
echo "Redeployment complete!"
echo "Your site is now running in the background."
echo "You can check the server console with: tmux attach -t $TMUX_SESSION"
echo "To detach from the session (and leave it running), press: Ctrl+b, then d"