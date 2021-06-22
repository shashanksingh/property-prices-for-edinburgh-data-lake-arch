resource "aws_instance" "airflow" {
  ami = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  associate_public_ip_address = true
  key_name = aws_key_pair.terraform-keys2.key_name
  subnet_id = aws_subnet.subnet-uno.id
  security_groups = [aws_security_group.ingress-all-test.id]

//  connection {
//    type     = "ssh"
//    user     = "root"
//    password = self.get_password_data
//    host     = self.public_dns
//  }
//  provisioner "remote-exec" {
//    inline = [
//      "ls",
//      "mkdir $HOME/code"
//    ]
//  }
//
//  provisioner "file" {
//    source      = "../workflow"
//    destination = "$HOME/code"
//
//  }

  tags={
    Name = "product"
    Environment = "production"
  }
}