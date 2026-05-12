variable "aws_region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "asterra"
}

variable "db_name" {
  default = "asterra_db"
}

variable "db_username" {
  default = "asterra_user"
}

variable "db_password" {
  default = "localstack_pass"
  sensitive = true
}

variable "localstack_endpoint" {
  default = "http://localhost:4566"
}
