#!/bin/sh
set -e
set -x

mkdir -p ~/.ssh
ssh-keyscan -H 10.0.18.23 >> ~/.ssh/known_hosts

ssh a@10.0.18.23 <<'EOF'
set -e
set -x

cd /home/a/gallereya/backend

if [ ! -d "env" ]; then
  echo "Creating Python venv..."
  python3.12 -m venv env
fi

make clean
rm /home/a/gallereya/backend/alembic/versions/*
EOF

rsync -avz \
  --exclude='env' \
  --exclude='.git' \
  --exclude='tests' \
  ./ a@10.0.18.23:/home/a/gallereya/backend

ssh a@10.0.18.23 <<'EOF'
set -e
set -x

cd /home/a/gallereya/backend

make install
make build

sudo /bin/systemctl restart gallereya-backend.service
EOF

echo "Deployment finished successfully."
