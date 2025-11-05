# Makefile for TV Scraper Project

.PHONY: help build up down logs status health clean dev prod scrape

# Default target
help:	## Show this help message
	@echo "TV Scraper Deployment Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build:	## Build Docker images
	docker build -t tv-scraper:latest .

up:	## Start all services in production mode
	docker-compose up -d

dev:	## Start services in development mode
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

down:	## Stop all services
	docker-compose down
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down 2>/dev/null || true

logs:	## Show logs from all services
	docker-compose logs -f

status:	## Show service status
	@echo "=== Docker Compose Status ==="
	docker-compose ps
	@echo ""
	@echo "=== Health Check ==="
	@curl -sf http://localhost:5001/health | python -m json.tool 2>/dev/null || echo "API not responding"

health:	## Check detailed health status
	@curl -sf http://localhost:5001/health/detailed | python -m json.tool 2>/dev/null || echo "Health endpoint not responding"

scrape:	## Run manual scraping job
	docker-compose run --rm scraper python /app/source/scheduler.py

clean:	## Remove all containers and volumes
	docker-compose down -v
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v 2>/dev/null || true
	docker system prune -f

# Production shortcuts
prod: build up	## Build and deploy in production mode

# Development shortcuts  
dev-full: build dev	## Build and deploy in development mode

# Quick restart
restart: down up	## Restart all services