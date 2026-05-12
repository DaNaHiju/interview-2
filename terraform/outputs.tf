output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "Public subnet ID"
  value       = aws_subnet.public.id
}

output "private_subnet_id" {
  description = "Private subnet ID"
  value       = aws_subnet.private.id
}

output "geojson_ingest_bucket" {
  description = "S3 bucket for GeoJSON ingestion"
  value       = aws_s3_bucket.geojson_ingest.id
}

output "iac_storage_bucket" {
  description = "S3 bucket for Terraform state"
  value       = aws_s3_bucket.iac_storage.id
}

output "public_halfpager_bucket" {
  description = "Public S3 bucket for half-pager"
  value       = aws_s3_bucket.public_halfpager.id
}

output "app_role_arn" {
  description = "IAM role ARN for the processing app"
  value       = aws_iam_role.app_role.arn
}
