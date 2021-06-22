output ip_server {
  value = aws_eip.airflow-eip.public_dns
}