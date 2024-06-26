# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update sources
sudo apt-get update

# Install python3 and Docker
sudo apt-get install -y make libpq-dev python3-full python3-pip docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker pull postgres

# Install python3 libs
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
