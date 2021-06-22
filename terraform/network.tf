resource "aws_vpc" "production-vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true
  tags= {
    Name = "production-vpc"
    Environment = "production"
  }
}

resource "aws_eip" "airflow-eip" {
  instance = aws_instance.airflow.id
  vpc      = true
  tags= {
    Name = "production-eip"
    Environment = "production"
  }
}