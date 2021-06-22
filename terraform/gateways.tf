resource "aws_internet_gateway" "production-gateway" {
  vpc_id = aws_vpc.production-vpc.id
  tags= {
    Name = "production-gateway"
    Environment = "production"
  }
}