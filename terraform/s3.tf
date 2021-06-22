resource "aws_s3_bucket" "datalake" {
  bucket = "property-prices-datalake"
  acl    = "private"

  tags = {
    Name        = "production-datalake"
    Environment = "production"
  }
}
