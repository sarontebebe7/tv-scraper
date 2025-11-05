# AWS Lambda function for periodic scraping
import json
import boto3
import subprocess
import os

def lambda_handler(event, context):
    """
    AWS Lambda function to run scrapers
    Triggered by EventBridge (CloudWatch Events) on schedule
    """
    
    # Download source code from S3 if needed
    # Run scraper
    # Upload results to S3
    # Trigger database update
    
    try:
        # Example: Run BBC scraper
        result = subprocess.run(['python', 'scraper_BBC.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Upload results to S3
            s3 = boto3.client('s3')
            s3.upload_file('tv_programs_BBC.txt', 'tv-scraper-bucket', 'data/tv_programs_BBC.txt')
            
            return {
                'statusCode': 200,
                'body': json.dumps('Scraping completed successfully')
            }
        else:
            raise Exception(f"Scraper failed: {result.stderr}")
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }