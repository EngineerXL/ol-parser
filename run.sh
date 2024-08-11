# Create data folder, if it does not exist
mkdir -p data

# Create config file, if it does not exist
if ! [ -f cfg/config.json ]; then
    echo "Creating example config..."
    cp cfg/example.json cfg/config.json
fi

# Start docker
echo "Starting docker container..."
docker compose run --rm parser $1

# Stop docker
echo "Shutting down docker container..."
docker compose down
