//variable "ami_key_pair_name" {}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
    owners = ["099720109477"] # Canonical
}


locals {
  amazon_linux_ami_two_id = "ami-0800fc0fa715fdcfe"
  ubuntu_server_twenty_zero_four = "amazon_linux_ami_two_id"
}