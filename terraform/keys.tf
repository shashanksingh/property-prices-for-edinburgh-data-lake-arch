resource "aws_key_pair" "terraform-keys2" {
  key_name = "terraform-keys2"
  public_key = file("${path.root}/terraform-keys2.pub")
}
