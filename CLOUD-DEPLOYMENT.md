# TV Scraper - AWS Cloud Deployment Guide

## 🚀 AWS ECS + Lambda Deployment

### Prerequisites
1. AWS CLI installed and configured
2. Docker installed locally  
3. AWS account with appropriate permissions

### Step 1: Build and Push Container Image

```bash
# Configure AWS ECR
aws ecr create-repository --repository-name tv-scraper

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag image
docker build -t tv-scraper:latest .
docker tag tv-scraper:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/tv-scraper:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/tv-scraper:latest
```

### Step 2: Deploy Infrastructure

```bash
# Deploy CloudFormation stack
aws cloudformation deploy \
  --template-file aws-cloudformation.yaml \
  --stack-name tv-scraper-stack \
  --parameter-overrides \
    DBPassword=YourSecurePassword123 \
    ImageURI=<account-id>.dkr.ecr.us-east-1.amazonaws.com/tv-scraper:latest \
  --capabilities CAPABILITY_IAM
```

### Step 3: Configure Environment

```bash
# Create RDS database tables
aws rds describe-db-instances --db-instance-identifier tv-scraper-db

# Update Lambda environment variables
aws lambda update-function-configuration \
  --function-name tv-scraper-function \
  --environment Variables="{S3_BUCKET=tv-scraper-data-bucket,DB_HOST=<rds-endpoint>}"
```

### Architecture Overview

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ EventBridge │───▶│ Lambda       │───▶│ S3 Storage  │
│ (Schedule)  │    │ (Scrapers)   │    │ (Results)   │
└─────────────┘    └──────────────┘    └─────────────┘
                           │
                           ▼
                   ┌──────────────┐    ┌─────────────┐
                   │ RDS Database │◀───│ ECS Service │
                   │ (PostgreSQL) │    │ (API Server)│
                   └──────────────┘    └─────────────┘
                           ▲                   │
                           │                   ▼
                   ┌──────────────┐    ┌─────────────┐
                   │ API Gateway  │◀───│ Load        │
                   │ (Public API) │    │ Balancer    │
                   └──────────────┘    └─────────────┘
```

### Estimated Costs (per month)
- ECS Service (Fargate): ~$15-30
- RDS db.t3.micro: ~$12-20  
- Lambda executions: ~$1-5
- S3 storage: ~$1-3
- **Total: ~$30-60/month**

## 🎯 Option 2: AWS Lambda + API Gateway (Serverless)

### Serverless Architecture
- Lambda functions for both scraping AND API
- DynamoDB for data storage
- API Gateway for HTTP endpoints
- EventBridge for scheduling

### Benefits
- Pay-per-use pricing
- Auto-scaling
- No server management
- Lower costs for low traffic

### Estimated Costs
- Lambda: ~$5-15/month
- DynamoDB: ~$5-10/month  
- API Gateway: ~$3-7/month
- **Total: ~$15-35/month**

## 🎯 Option 3: Kubernetes (EKS)

### For Large Scale Deployments
- Full Kubernetes orchestration
- Multi-region deployment
- Advanced monitoring and scaling
- Higher costs but maximum flexibility

### Estimated Costs
- EKS Cluster: ~$75/month
- Worker nodes: ~$50-150/month
- **Total: ~$125-225/month**

## 🎯 Option 4: Simple VPS Deployment

### Budget-Friendly Option
- Single VPS instance
- Docker Compose deployment
- Manual scaling
- Basic monitoring

### Providers & Costs
- DigitalOcean Droplet: $12-24/month
- AWS EC2 t3.small: $15-20/month
- Google Cloud e2-small: $13-18/month

## 📋 Deployment Checklist

### Before Deploying
- [ ] Choose deployment option
- [ ] Set up AWS credentials
- [ ] Configure domain name (optional)
- [ ] Set up monitoring/alerting
- [ ] Plan backup strategy

### Security Considerations
- [ ] Use AWS IAM roles (not access keys)
- [ ] Enable VPC security groups
- [ ] Set up SSL/TLS certificates
- [ ] Configure database encryption
- [ ] Enable CloudWatch logging

### Post-Deployment
- [ ] Test all API endpoints
- [ ] Verify scraper scheduling
- [ ] Set up monitoring dashboards
- [ ] Configure alerts for failures
- [ ] Document API endpoints for users

## 🚀 Quick Start Commands

```bash
# Clone and prepare
git clone <your-repo>
cd tv-program-web-scraper

# Option 1: AWS ECS Deployment
./deploy.sh aws-ecs

# Option 2: Serverless Deployment  
./deploy.sh aws-serverless

# Option 3: Simple VPS
./deploy.sh vps

# Check deployment status
aws ecs describe-services --cluster tv-scraper-cluster
```

## 📞 Support

After deployment, your API will be available at:
- **AWS**: https://<api-gateway-id>.execute-api.us-east-1.amazonaws.com/
- **VPS**: https://your-domain.com:5001/

### API Endpoints
- `GET /now-playing` - Current TV programs
- `GET /viewers` - Live viewer counts  
- `GET /status` - System health
- `GET /subscribe` - SSE stream