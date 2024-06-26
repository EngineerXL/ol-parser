# Activate venv
python3 -m venv .venv
source .venv/bin/activate

# Start docker
echo "Starting docker container..."
docker compose up -d

# Wait for 5 seconds to let PostgreSQL initialize
echo "Initializing PostgreSQL..."
sleep 5

echo "Running script..."
python3 main.py $1

echo "Shutting down docker container..."
docker compose down
