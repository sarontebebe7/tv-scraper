"""
Health monitoring endpoints for the TV Scraper API
"""
import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "tv-scraper-api"
    })

@health_bp.route('/health/detailed')
def detailed_health():
    """Detailed health check with component status"""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {}
    }
    
    overall_status = "healthy"
    
    # Check database
    try:
        db_path = os.getenv('DB_PATH', 'tvguide.db')
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM program_info")
            program_count = cursor.fetchone()[0]
            cursor = conn.execute("SELECT COUNT(*) FROM program_schedule")
            schedule_count = cursor.fetchone()[0]
            conn.close()
            
            health_data["components"]["database"] = {
                "status": "healthy",
                "program_count": program_count,
                "schedule_count": schedule_count,
                "last_modified": datetime.fromtimestamp(os.path.getmtime(db_path)).isoformat()
            }
        else:
            health_data["components"]["database"] = {
                "status": "error",
                "message": "Database file not found"
            }
            overall_status = "degraded"
    except Exception as e:
        health_data["components"]["database"] = {
            "status": "error",
            "message": str(e)
        }
        overall_status = "degraded"
    
    # Check scheduler status
    try:
        status_file = Path('/app/data/scheduler_status.json')
        if status_file.exists():
            with open(status_file) as f:
                scheduler_status = json.load(f)
            
            # Check if status is recent (within last 2 hours)
            status_time = datetime.fromisoformat(scheduler_status['timestamp'])
            if datetime.now() - status_time > timedelta(hours=2):
                scheduler_status['status'] = 'stale'
                scheduler_status['message'] = 'Status file is outdated'
                overall_status = "degraded"
            
            health_data["components"]["scheduler"] = scheduler_status
        else:
            health_data["components"]["scheduler"] = {
                "status": "unknown",
                "message": "Scheduler status file not found"
            }
            overall_status = "degraded"
    except Exception as e:
        health_data["components"]["scheduler"] = {
            "status": "error",
            "message": str(e)
        }
        overall_status = "degraded"
    
    # Check data files
    data_files = ['tv_programs_BBC.txt', 'tv_programs_Disc.txt', 'tv_programs_NatGeo.txt']
    file_status = {}
    
    for file_name in data_files:
        file_path = f'/app/source/{file_name}'
        if os.path.exists(file_path):
            file_status[file_name] = {
                "status": "present",
                "size": os.path.getsize(file_path),
                "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
            }
        else:
            file_status[file_name] = {
                "status": "missing"
            }
            overall_status = "degraded"
    
    health_data["components"]["data_files"] = file_status
    health_data["status"] = overall_status
    
    return jsonify(health_data)

@health_bp.route('/metrics')
def metrics():
    """Prometheus-style metrics endpoint"""
    metrics_data = []
    
    try:
        # Database metrics
        db_path = os.getenv('DB_PATH', 'tvguide.db')
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            
            # Program count
            cursor = conn.execute("SELECT COUNT(*) FROM program_info")
            program_count = cursor.fetchone()[0]
            metrics_data.append(f"tv_scraper_programs_total {program_count}")
            
            # Schedule count
            cursor = conn.execute("SELECT COUNT(*) FROM program_schedule")
            schedule_count = cursor.fetchone()[0]
            metrics_data.append(f"tv_scraper_schedules_total {schedule_count}")
            
            # Programs by channel
            cursor = conn.execute("SELECT channel, COUNT(*) FROM program_info GROUP BY channel")
            for channel, count in cursor.fetchall():
                safe_channel = channel.replace(' ', '_').replace('-', '_').lower()
                metrics_data.append(f'tv_scraper_programs_by_channel{{channel="{channel}"}} {count}')
            
            conn.close()
        
        # Service uptime (simplified)
        metrics_data.append(f"tv_scraper_service_up 1")
        
    except Exception as e:
        metrics_data.append(f"tv_scraper_service_up 0")
        metrics_data.append(f"# Error: {str(e)}")
    
    return '\n'.join(metrics_data), 200, {'Content-Type': 'text/plain'}

@health_bp.route('/status')
def status():
    """Service status summary"""
    try:
        # Get basic stats
        db_path = os.getenv('DB_PATH', 'tvguide.db')
        stats = {"database": "not_found"}
        
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM program_info")
            program_count = cursor.fetchone()[0]
            cursor = conn.execute("SELECT COUNT(*) FROM program_schedule")
            schedule_count = cursor.fetchone()[0]
            
            # Get latest schedule entry
            cursor = conn.execute("SELECT MAX(timestamp) FROM program_schedule")
            latest_update = cursor.fetchone()[0]
            
            conn.close()
            
            stats = {
                "database": "connected",
                "programs": program_count,
                "schedules": schedule_count,
                "last_update": latest_update,
                "channels": ["BBC Earth", "Discovery Channel", "National Geographic"]
            }
        
        return jsonify({
            "service": "TV Program Scraper API",
            "version": "1.0.0",
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "stats": stats
        })
        
    except Exception as e:
        return jsonify({
            "service": "TV Program Scraper API",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500