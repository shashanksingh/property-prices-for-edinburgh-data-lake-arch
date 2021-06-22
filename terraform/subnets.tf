resource "aws_subnet" "subnet-uno" {
  cidr_block = cidrsubnet(aws_vpc.production-vpc.cidr_block, 3, 1)
  vpc_id = aws_vpc.production-vpc.id
  tags= {
    Name = "production-subnet"
    Environment = "production"
  }
}

resource "aws_route_table" "route-table" {
  vpc_id = aws_vpc.production-vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.production-gateway.id
  }
  tags= {
    Name = "production-route-table"
    Environment = "production"
  }
}

resource "aws_route_table_association" "subnet-association" {
  subnet_id      = aws_subnet.subnet-uno.id
  route_table_id = aws_route_table.route-table.id
}