#!/bin/bash

echo "Downloading anaconda..."
wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh

echo "Running the anaconda script..."
bash Anaconda3-2024.02-1-Linux-x86_64.sh -b -p ~/anaconda

echo "Removing anaconda script..."
rm Anaconda3-2024.02-1-Linux-x86_64.sh

#activate conda
eval "$($HOME/anaconda/bin/conda shell.bash hook)"

echo "Running conda init..."
conda init
# Using -y flag to auto-approve
echo "Running conda update..."
conda update -y conda

echo "Installed conda version..."
conda --version

echo "Updating apt-get version..."
sudo apt-get update

echo "Installing Docker..."
sudo apt-get -y install docker.io

echo "Setting up Docker to run without sudo..."
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart

echo "Installing docker-compose..."
cd 
mkdir -p bin
cd bin
wget https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -O docker-compose
sudo chmod +x docker-compose

echo "Adding PATH variables to .bashrc..."
echo '' >> ~/.bashrc
echo 'export PATH=${HOME}/bin:${PATH}' >> ~/.bashrc
eval "$(cat ~/.bashrc | tail -n +10)" # A hack because source .bashrc doesn't work inside the script

echo "docker-compose version..."
docker-compose --version

exec bash

cd bin
echo "Installing Terraform"
wget https://releases.hashicorp.com/terraform/1.7.5/terraform_1.7.5_linux_amd64.zip

echo "Installing unzip"
sudo apt-get install unzip

echo "Unzipping Terraform"
unzip terraform_1.7.5_linux_amd64.zip

echo "Removing Terraform zip file"
rm terraform_1.7.5_linux_amd64.zip

terraform --version
