#!/bin/bash
# deploy.sh - Main deployment script for TV Scraper

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker Desktop first."
        echo "Download from: https://docs.docker.com/desktop/install/windows/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    
    print_success "Docker is available and running"
}

# Build the Docker image
build_image() {
    print_status "Building TV Scraper Docker image..."
    
    if docker build -t tv-scraper:latest .; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Deploy in production mode
deploy_production() {
    print_status "Deploying TV Scraper in production mode..."
    
    # Stop existing containers
    docker-compose down 2>/dev/null || true
    
    # Start services
    if docker-compose up -d; then
        print_success "Production deployment completed"
        
        # Wait for services to be healthy
        print_status "Waiting for services to become healthy..."
        sleep 30
        
        # Check service status
        if docker-compose ps | grep -q "Up"; then
            print_success "Services are running"
            
            # Show service URLs
            echo
            print_status "Service URLs:"
            echo "  API Server: http://localhost:5001"
            echo "  Health Check: http://localhost:5001/health"
            echo "  Now Playing: http://localhost:5001/now-playing"
            echo "  Metrics: http://localhost:5001/metrics"
        else
            print_error "Some services failed to start"
            docker-compose logs
        fi
    else
        print_error "Failed to start services"
        exit 1
    fi
}

# Deploy in development mode
deploy_development() {
    print_status "Deploying TV Scraper in development mode..."
    
    # Stop existing containers
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml down 2>/dev/null || true
    
    # Start development services
    if docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d; then
        print_success "Development deployment completed"
        
        echo
        print_status "Development URLs:"
        echo "  API Server: http://localhost:5001"
        echo "  SQLite Browser: http://localhost:8080 (run with --profile browser)"
    else
        print_error "Failed to start development services"
        exit 1
    fi
}

# Show logs
show_logs() {
    print_status "Showing logs for all services..."
    docker-compose logs -f
}

# Stop all services
stop_services() {
    print_status "Stopping all TV Scraper services..."
    docker-compose down
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml down 2>/dev/null || true
    print_success "All services stopped"
}

# Run manual scraping
run_manual_scrape() {
    print_status "Running manual scraping job..."
    
    if docker-compose run --rm scraper python /app/source/scheduler.py; then
        print_success "Manual scraping completed"
    else
        print_error "Manual scraping failed"
        exit 1
    fi
}

# Show help
show_help() {
    echo "TV Scraper Deployment Script"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  prod, production     Deploy in production mode"
    echo "  dev, development     Deploy in development mode"  
    echo "  build               Build Docker image only"
    echo "  logs                Show logs from all services"
    echo "  stop                Stop all services"
    echo "  scrape              Run manual scraping job"
    echo "  status              Show service status"
    echo "  help                Show this help message"
}

# Show service status
show_status() {
    print_status "Service Status:"
    docker-compose ps
    
    echo
    print_status "Health Check:"
    if curl -sf http://localhost:5001/health > /dev/null 2>&1; then
        print_success "API Server is healthy"
        curl -s http://localhost:5001/status | python -m json.tool 2>/dev/null || echo "API responded but JSON parsing failed"
    else
        print_warning "API Server is not responding"
    fi
}

# Main script logic
main() {
    case "${1:-help}" in
        "prod"|"production")
            check_docker
            build_image
            deploy_production
            ;;
        "dev"|"development")
            check_docker
            build_image
            deploy_development
            ;;
        "build")
            check_docker
            build_image
            ;;
        "logs")
            show_logs
            ;;
        "stop")
            stop_services
            ;;
        "scrape")
            run_manual_scrape
            ;;
        "status")
            show_status
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

main "$@"