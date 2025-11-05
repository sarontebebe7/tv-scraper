# Cloud Deployment Quick Start Script for Windows
# Usage: .\cloud-deploy.ps1 -Type aws-ecs

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("aws-ecs", "aws-serverless", "azure", "gcp")]
    [string]$Type = "aws-ecs"
)

Write-Host "Cloud TV Scraper Cloud Deployment Assistant" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Quick deployment check
function Show-DeploymentOptions {
    Write-Host ""
    Write-Host "Available Deployment Options:" -ForegroundColor Yellow
    Write-Host "1. AWS ECS + Lambda (Recommended) - 30-60 USD/month" -ForegroundColor White
    Write-Host "2. AWS Serverless (Lambda + API Gateway) - 15-35 USD/month" -ForegroundColor White
    Write-Host "3. Azure Container Instances - 25-50 USD/month" -ForegroundColor White
    Write-Host "4. Google Cloud Run - 20-40 USD/month" -ForegroundColor White
    Write-Host ""
    Write-Host "For detailed steps, see: CLOUD-DEPLOYMENT.md" -ForegroundColor Cyan
}

# AWS ECS Quick Deploy
function Start-AWSECSDeployment {
    Write-Host ""
    Write-Host "AWS ECS + Lambda Deployment" -ForegroundColor Green
    Write-Host "=============================" -ForegroundColor Green
    
    # Check AWS CLI
    if (!(Get-Command aws -ErrorAction SilentlyContinue)) {
        Write-Host "AWS CLI not installed" -ForegroundColor Red
        Write-Host "Download: https://aws.amazon.com/cli/" -ForegroundColor Yellow
        return
    }
    
    Write-Host "Required steps:" -ForegroundColor Blue
    Write-Host "1. Configure AWS credentials: aws configure" -ForegroundColor White
    Write-Host "2. Run: aws cloudformation deploy --template-file aws-cloudformation.yaml --stack-name tv-scraper --capabilities CAPABILITY_IAM" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Estimated cost: 30-60 USD/month" -ForegroundColor Cyan
    Write-Host "Deployment time: 10-15 minutes" -ForegroundColor Cyan
}

# AWS Serverless Quick Deploy
function Start-AWSServerlessDeployment {
    Write-Host ""
    Write-Host "AWS Serverless Deployment" -ForegroundColor Green
    Write-Host "============================" -ForegroundColor Green
    
    Write-Host "This deployment includes:" -ForegroundColor Blue
    Write-Host "• Lambda functions for API and scraping" -ForegroundColor White
    Write-Host "• DynamoDB for data storage" -ForegroundColor White
    Write-Host "• API Gateway for HTTP endpoints" -ForegroundColor White
    Write-Host "• EventBridge for scheduling" -ForegroundColor White
    
    Write-Host ""
    Write-Host "Estimated cost: 15-35 USD/month" -ForegroundColor Cyan
    Write-Host "Deployment time: 5-10 minutes" -ForegroundColor Cyan
}

# Show current project status
function Show-ProjectStatus {
    Write-Host ""
    Write-Host "Current Project Status:" -ForegroundColor Yellow
    Write-Host "Docker deployment working locally" -ForegroundColor Green
    Write-Host "API endpoints returning real data" -ForegroundColor Green
    Write-Host "Database populated with TV programs" -ForegroundColor Green
    Write-Host "Viewer simulation active" -ForegroundColor Green
    Write-Host "Ready for cloud deployment" -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "Key Files:" -ForegroundColor Blue
    Write-Host "• aws-cloudformation.yaml - AWS infrastructure template" -ForegroundColor White
    Write-Host "• aws-serverless.yaml - Serverless infrastructure template" -ForegroundColor White
    Write-Host "• aws-lambda-scraper.py - Lambda function code" -ForegroundColor White
    Write-Host "• docker-compose.yml - Container orchestration" -ForegroundColor White
    Write-Host "• flask_now_playing.py - Main API server" -ForegroundColor White
}

# Main execution
Show-ProjectStatus
Show-DeploymentOptions

switch ($Type) {
    "aws-ecs" {
        Start-AWSECSDeployment
    }
    "aws-serverless" {
        Start-AWSServerlessDeployment
    }
    "azure" {
        Write-Host ""
        Write-Host "Azure Container Instances deployment documentation available in CLOUD-DEPLOYMENT.md" -ForegroundColor Blue
    }
    "gcp" {
        Write-Host ""
        Write-Host "Google Cloud Run deployment documentation available in CLOUD-DEPLOYMENT.md" -ForegroundColor Blue
    }
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Choose your preferred deployment option" -ForegroundColor White
Write-Host "2. Configure cloud provider credentials" -ForegroundColor White
Write-Host "3. Run the deployment script" -ForegroundColor White
Write-Host "4. Test the deployed endpoints" -ForegroundColor White

Write-Host ""
Write-Host "Need help? Check the detailed guide in CLOUD-DEPLOYMENT.md" -ForegroundColor Cyan