resource "aws_security_group" "ingress-all-test" {
  name = "allow-all-sg"
  vpc_id = aws_vpc.production-vpc.id
  description = "Allow HTTP, HTTPS and SSH traffic"

  //for ssh to confirm installation
  // and see logs
  ingress {
    cidr_blocks = [
      "0.0.0.0/0"
    ]
    from_port = 22
    to_port = 22
    protocol = "tcp"
  }

  //for airflow web
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  // Terraform removes the default rule
  egress {
   from_port = 0
   to_port = 0
   protocol = "-1"
   cidr_blocks = ["0.0.0.0/0"]
 }

  tags={
    Name = "production-security-group"
    Environment = "production"
  }
}