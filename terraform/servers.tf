resource "aws_instance" "airflow" {
  ami = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  associate_public_ip_address = true
  key_name = aws_key_pair.terraform-keys2.key_name
  subnet_id = aws_subnet.subnet-uno.id
  security_groups = [aws_security_group.ingress-all-test.id]

  connection {
    type        = "ssh"
    user        = "ubuntu"
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
    destination = "$HOME/code"
  }

  provisioner "file" {
    source      = "../workflow/Makefile"
    destination = "$HOME/code"
  }
  user_data = <<EOF
#!/bin/sh
sudo apt-get update
sudo apt-get install -y docker-compose
make dev-setup
make dev-run
EOF

  tags={
    Name = "product"
    Environment = "production"
  }
}