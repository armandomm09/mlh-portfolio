#!/bin/bash

PROJECT_DIR="/root/mlh-portfolio"
START_SCRIPT="/root/start_server.sh"

echo "Starting redeployment process..."


echo "-> Stopping portfolio container"
docker compose -f docker-compose.prod.yaml down
echo "Done."

cd "$PROJECT_DIR" || { echo "Error: Project directory not found. Aborting."; exit 1; }
echo "Done."

echo "Fetching the latest code from GitHub..."
git fetch origin
git reset --hard origin/main
echo "Done."

docker compose -f docker-compose.prod.yaml up -d --build

chmod +x /root/mlh-portfolio/scripts/redeploy-site.sh
echo ""
echo "Redeployment complete!"
echo "Your site is now running in the background."
echo "You can check the website at https://armando-mlh-portfolio.duckdns.org/"