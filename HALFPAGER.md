# ASTERRA DevOps Assignment — Implementation Write-up

## Overview
[2-3 sentences: What did you build? What problem does it solve?]

## Architecture

[1 paragraph describing: VPC → subnets → security groups → S3 → processing app → RDS/PostGIS]

### Data Flow
[Describe: GeoJSON lands in S3 → triggers app → validates → loads into PostGIS]

## Key Technical Decisions

- **LocalStack for AWS simulation**: [Why? Cost, speed, local testing...]
- **Docker Compose for local dev**: [Why? Easy orchestration, mirrors prod...]
- **PostgreSQL + PostGIS in container**: [Why? RDS not available in LocalStack free tier...]
- **Python/Flask for processing**: [Why? Simple, handles JSON well, GeoPandas...]

## Challenges & Solutions

- **Challenge 1**: [What went wrong and how you fixed it]
- **Challenge 2**: [What went wrong and how you fixed it]

## How to Reproduce

1. `export LOCALSTACK_AUTH_TOKEN=...`
2. `localstack start -d`
3. `docker compose up -d`
4. `cd terraform && terraform apply`
5. Test: `awslocal s3 cp test.geojson s3://asterra-geojson-ingest/ && curl -X POST http://localhost:5000/process/...`

## If Deploying to Real AWS

Comment out in `.github/workflows/ci.yml`:
- ECR push section
- Terraform apply section

Uncomment when you have real AWS credentials.

## Future Improvements

- [ ] Kubernetes deployment (k3s)
- [ ] Auto-scaling based on S3 upload rate
- [ ] Web UI for monitoring processing status
- [ ] Webhook notifications on completion
