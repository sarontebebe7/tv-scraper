# deploy.ps1 - PowerShell deployment script for TV Scraper
param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

# Color output functions
function Write-Status { 
    Write-Host "[INFO] $args" -ForegroundColor Blue 
}
function Write-Success { 
    Write-Host "[SUCCESS] $args" -ForegroundColor Green 
}
function Write-Warning { 
    Write-Host "[WARNING] $args" -ForegroundColor Yellow 
}
function Write-Error { 
    Write-Host "[ERROR] $args" -ForegroundColor Red 
}

# Check if Docker is installed and running
function Test-Docker {
    try {
        $null = docker --version
        if ($LASTEXITCODE -ne 0) {
            throw "Docker command failed"
        }
    }
    catch {
        Write-Error "Docker is not installed. Please install Docker Desktop first."
        Write-Host "Download from: https://docs.docker.com/desktop/install/windows/"
        exit 1
    }
    
    try {
        $null = docker info 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Docker info failed"
        }
    }
    catch {
        Write-Error "Docker is not running. Please start Docker Desktop."
        exit 1
    }
    
    Write-Success "Docker is available and running"
}

# Build the Docker image
function Build-Image {
    Write-Status "Building TV Scraper Docker image..."
    
    docker build -t tv-scraper:latest .
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Docker image built successfully"
    }
    else {
        Write-Error "Failed to build Docker image"
        exit 1
    }
}

# Deploy in production mode
function Deploy-Production {
    Write-Status "Deploying TV Scraper in production mode..."
    
    # Stop existing containers
    docker-compose down 2>$null
    
    # Start services
    docker-compose up -d
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Production deployment completed"
        
        # Wait for services to be healthy
        Write-Status "Waiting for services to become healthy..."
        Start-Sleep -Seconds 30
        
        # Check service status
        $status = docker-compose ps
        if ($status -match "Up") {
            Write-Success "Services are running"
            
            # Show service URLs
            Write-Host ""
            Write-Status "Service URLs:"
            Write-Host "  API Server: http://localhost:5001"
            Write-Host "  Health Check: http://localhost:5001/health"
            Write-Host "  Now Playing: http://localhost:5001/now-playing"
            Write-Host "  Metrics: http://localhost:5001/metrics"
        }
        else {
            Write-Error "Some services failed to start"
            docker-compose logs
        }
    }
    else {
        Write-Error "Failed to start services"
        exit 1
    }
}

# Deploy in development mode
function Deploy-Development {
    Write-Status "Deploying TV Scraper in development mode..."
    
    # Stop existing containers
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml down 2>$null
    
    # Start development services
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Development deployment completed"
        
        Write-Host ""
        Write-Status "Development URLs:"
        Write-Host "  API Server: http://localhost:5001"
        Write-Host "  SQLite Browser: http://localhost:8080 (run with --profile browser)"
    }
    else {
        Write-Error "Failed to start development services"
        exit 1
    }
}

# Show logs
function Show-Logs {
    Write-Status "Showing logs for all services..."
    docker-compose logs -f
}

# Stop all services
function Stop-Services {
    Write-Status "Stopping all TV Scraper services..."
    docker-compose down
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml down 2>$null
    Write-Success "All services stopped"
}

# Run manual scraping
function Invoke-ManualScrape {
    Write-Status "Running manual scraping job..."
    
    docker-compose run --rm scraper python /app/source/scheduler.py
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Manual scraping completed"
    }
    else {
        Write-Error "Manual scraping failed"
        exit 1
    }
}

# Show service status
function Show-Status {
    Write-Status "Service Status:"
    docker-compose ps
    
    Write-Host ""
    Write-Status "Health Check:"
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:5001/health" -TimeoutSec 5
        Write-Success "API Server is healthy"
        $response | ConvertTo-Json -Depth 3
    }
    catch {
        Write-Warning "API Server is not responding"
    }
}

# Show help
function Show-Help {
    Write-Host "TV Scraper Deployment Script"
    Write-Host ""
    Write-Host "Usage: .\deploy.ps1 [COMMAND]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  prod, production     Deploy in production mode"
    Write-Host "  dev, development     Deploy in development mode"
    Write-Host "  build               Build Docker image only"
    Write-Host "  logs                Show logs from all services"
    Write-Host "  stop                Stop all services"
    Write-Host "  scrape              Run manual scraping job"
    Write-Host "  status              Show service status"
    Write-Host "  help                Show this help message"
}

# Main script logic
switch ($Command.ToLower()) {
    { $_ -in @("prod", "production") } {
        Test-Docker
        Build-Image
        Deploy-Production
    }
    { $_ -in @("dev", "development") } {
        Test-Docker
        Build-Image
        Deploy-Development
    }
    "build" {
        Test-Docker
        Build-Image
    }
    "logs" {
        Show-Logs
    }
    "stop" {
        Stop-Services
    }
    "scrape" {
        Invoke-ManualScrape
    }
    "status" {
        Show-Status
    }
    default {
        Show-Help
    }
}