#!/bin/bash

sudo yum update -y

# Install docker
sudo amazon-linux-extras install -y docker
sudo service docker start
sudo usermod -aG docker $USER
sudo chkconfig docker on
sudo yum install -y git
newgrp docker
