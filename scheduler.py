import schedule
import time
import subprocess
import logging
import os
import json
from datetime import datetime
from pathlib import Path

# Setup logging with better formatting
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/data/scheduler.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Configuration from environment
SCRAPING_INTERVAL = int(os.getenv('SCRAPING_INTERVAL_HOURS', 6))
DB_PATH = os.getenv('DB_PATH', '/app/data/tvguide.db')

def create_status_file(status, message=""):
    """Create a status file for health checks"""
    status_data = {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "message": message
    }
    
    status_file = Path('/app/data/scheduler_status.json')
    with open(status_file, 'w') as f:
        json.dump(status_data, f, indent=2)

def run_scraper(scraper_name):
    """Run a specific scraper with better error handling"""
    try:
        logger.info(f"Starting {scraper_name} scraper...")
        
        result = subprocess.run(
            ['python', f'scraper_{scraper_name}.py'], 
            capture_output=True, 
            text=True, 
            timeout=3600,
            cwd='/app'
        )
        
        if result.returncode == 0:
            logger.info(f"{scraper_name} scraper completed successfully")
            
            # Check if output file was created
            output_file = f'tv_programs_{scraper_name}.txt'
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                logger.info(f"{scraper_name} output file size: {file_size} bytes")
            else:
                logger.warning(f"{scraper_name} output file not found")
                
            return True
        else:
            logger.error(f"{scraper_name} scraper failed with code {result.returncode}")
            logger.error(f"Stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"{scraper_name} scraper timed out after 1 hour")
        return False
    except Exception as e:
        logger.error(f"Unexpected error running {scraper_name} scraper: {e}")
        return False

def run_all_scrapers():
    """Run all scrapers and update database with comprehensive logging"""
    start_time = datetime.now()
    logger.info("=== Starting scheduled scraping job ===")
    
    create_status_file("running", "Scraping in progress")
    
    try:
        # Run all scrapers
        scrapers = ['BBC', 'Disc', 'NatGeo']
        success_count = 0
        
        for scraper in scrapers:
            if run_scraper(scraper):
                success_count += 1
            else:
                logger.warning(f"Scraper {scraper} failed, continuing with others")
        
        logger.info(f"Scraping completed: {success_count}/{len(scrapers)} scrapers successful")
        
        if success_count == 0:
            logger.error("All scrapers failed, skipping database update")
            create_status_file("error", "All scrapers failed")
            return
        
        # Load data into database
        logger.info("Loading data into database...")
        result = subprocess.run(
            ['python', 'load_tv_programs_sqlite.py'], 
            capture_output=True, 
            text=True, 
            timeout=300,
            cwd='/app'
        )
        
        if result.returncode == 0:
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Database update completed successfully in {duration:.1f} seconds")
            
            # Check database file
            if os.path.exists(DB_PATH):
                db_size = os.path.getsize(DB_PATH)
                logger.info(f"Database file size: {db_size} bytes")
            
            create_status_file("success", f"Job completed in {duration:.1f}s with {success_count}/{len(scrapers)} scrapers")
        else:
            logger.error(f"Database update failed: {result.stderr}")
            create_status_file("error", "Database update failed")
            
    except Exception as e:
        logger.error(f"Fatal error in scraping job: {e}")
        create_status_file("error", f"Fatal error: {str(e)}")
    
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"=== Scheduled scraping job completed in {duration:.1f} seconds ===")

def main():
    logger.info("TV Program Scheduler started")
    logger.info(f"Scraping interval: {SCRAPING_INTERVAL} hours")
    logger.info(f"Database path: {DB_PATH}")
    
    # Ensure data directory exists
    os.makedirs('/app/data', exist_ok=True)
    
    create_status_file("starting", "Scheduler initializing")
    
    # Schedule scraping jobs
    schedule.every(SCRAPING_INTERVAL).hours.do(run_all_scrapers)
    schedule.every().day.at("06:00").do(run_all_scrapers)
    
    # Run once at startup
    logger.info("Running initial scraping job...")
    run_all_scrapers()
    
    create_status_file("ready", "Scheduler running normally")
    
    # Keep the scheduler running
    logger.info("Scheduler ready, waiting for scheduled jobs...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            create_status_file("stopped", "Scheduler stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in scheduler loop: {e}")
            create_status_file("error", f"Scheduler error: {str(e)}")
            time.sleep(60)  # Continue after errors

if __name__ == "__main__":
    main()