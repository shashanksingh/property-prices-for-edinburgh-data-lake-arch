resource "aws_instance" "airflow" {
  ami = local.amazon_linux_ami_two_id
  instance_type = "t3.micro"
  associate_public_ip_address = true
  key_name = aws_key_pair.terraform-keys2.key_name
  subnet_id = aws_subnet.subnet-uno.id
  security_groups = [aws_security_group.ingress-all-test.id]

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file("${path.root}/terraform-keys2")
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "ls",
      "mkdir $HOME/code",
      "mkdir $HOME/code/dags"
    ]
  }

  provisioner "file" {
    source      = "../workflow/dags/"
    destination = "$HOME/code/dags"
  }

  provisioner "file" {
    source      = "../workflow/docker-compose.yaml"
    destination = "$HOME/code/docker-compose.yaml"
  }

  provisioner "file" {
    source      = "../workflow/Makefile"
    destination = "$HOME/code/Makefile"
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir -p $HOME/code/logs $HOME/code/plugins",
      "echo \"AIRFLOW_UID=$(shell id -u)\nAIRFLOW_GID=0\" > $HOME/code/.env",
      "sudo yum update -y",
      "sudo amazon-linux-extras install -y docker",
      "sudo service docker start",
      "sudo usermod -a -G docker ec2-user",
      "sudo chkconfig docker on",
      "sudo yum install -y git",
      "sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose",
      "cd $HOME/code && docker-compose up"
    ]
  }

//  user_data = <<EOF
//#!/bin/sh
//EOF

  tags={
    Name = "product"
    Environment = "production"
  }
}