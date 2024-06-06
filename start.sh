echo "Starting docker container..."
docker-compose up -d

# Нужно подождать, чтобы PostgreSQL успел инициализироваться
echo "Initializing PostgreSQL..."
sleep 5

echo "Running script..."
python3 main.py $1

echo "Shutting down docker container..."
docker-compose down
