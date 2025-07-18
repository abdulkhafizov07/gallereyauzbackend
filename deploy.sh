#!/bin/sh
set -e
set -x

echo "Starting deploy process..."

echo "Setting up SSH known_hosts..."
mkdir -p ~/.ssh
ssh-keyscan -H 10.0.18.23 >> ~/.ssh/known_hosts
echo "Server keys added to known_hosts"

echo "Syncing project to remote server..."
rsync -avz \
  --exclude='env' \
  --exclude='.git' \
  --exclude='tests'
  ./ a@10.0.18.23:/home/a/gallereya/backend

echo "Project synced."

echo "Executing remote deployment tasks..."

ssh a@10.0.18.23 <<'EOF'
set -e
set -x

cd /home/a/gallereya/backend

echo "Checking virtual environment..."
if [ ! -d "env" ]; then
  echo "Creating Python venv..."
  python3.12 -m venv env
fi

echo "Installing requirements..."
env/bin/pip install --upgrade pip
env/bin/pip install -r requirements.txt

echo "Running Alembic migrations..."
env/bin/alembic upgrade head

echo "Restarting systemd service..."
sudo /bin/systemctl restart gallereya-backend.service

echo "Remote deployment complete!"
EOF

echo "Deployment finished successfully."
