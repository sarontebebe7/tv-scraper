# TV Program Web Scraper - Docker Deployment

A modernized deployment system for the TV Program Web Scraper project, replacing SLURM with Docker containers for better portability and ease of deployment.

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://docs.docker.com/desktop/install/windows/) for Windows
- PowerShell 5.1+ (included with Windows)

### Deploy in 3 Steps

1. **Install Docker Desktop** (if not already installed)
2. **Clone and navigate to project**:
   ```powershell
   cd "C:\Users\saron\Downloads\tv-program-web-scraper-main\tv-program-web-scraper-main"
   ```
3. **Deploy**:
   ```powershell
   .\deploy.ps1 prod
   ```

## 📋 Available Commands

### Windows (PowerShell)
```powershell
.\deploy.ps1 prod          # Production deployment
.\deploy.ps1 dev           # Development deployment  
.\deploy.ps1 build         # Build Docker image only
.\deploy.ps1 logs          # Show service logs
.\deploy.ps1 status        # Check service status
.\deploy.ps1 stop          # Stop all services
.\deploy.ps1 scrape        # Run manual scraping
```

### Alternative: Make commands (if you have Make installed)
```bash
make prod                  # Production deployment
make dev                   # Development deployment
make build                 # Build Docker image
make logs                  # Show logs
make status                # Service status
make clean                 # Clean up everything
```

## 🏗️ Architecture

### Services Overview

| Service | Purpose | Port | Health Check |
|---------|---------|------|--------------|
| **api-server** | Flask API for data access | 5001 | `/health` |
| **scheduler** | Periodic scraping & DB updates | - | Status file |
| **scraper** | Manual scraping (on-demand) | - | N/A |

### Data Flow
```
Scheduler → Scrapers (BBC/Discovery/NatGeo) → SQLite DB → Flask API → External Consumers
```

## 🌐 API Endpoints

Once deployed, access these endpoints at `http://localhost:5001`:

### Data Endpoints
- `GET /now-playing` - Current TV programs
- `GET /viewers` - Real-time viewer counts
- `GET /subscribe` - SSE stream for live updates

### Monitoring Endpoints  
- `GET /health` - Basic health check
- `GET /health/detailed` - Comprehensive health status
- `GET /status` - Service status summary
- `GET /metrics` - Prometheus-style metrics

### Example Usage
```powershell
# Get current programs
Invoke-RestMethod http://localhost:5001/now-playing

# Check health
Invoke-RestMethod http://localhost:5001/health

# Get detailed status
Invoke-RestMethod http://localhost:5001/status
```

## 🔧 Configuration

### Environment Variables
Edit `.env` file to customize:

```env
# Scraping settings
SCRAPING_INTERVAL_HOURS=6
DETAIL_DELAY_SEC=0.5

# Database settings  
DB_PATH=/app/data/tvguide.db

# API settings
API_HOST=0.0.0.0
API_PORT=5001

# Logging
LOG_LEVEL=INFO
```

### Development vs Production

**Production Mode:**
- Optimized for stability
- Automatic restarts
- Health monitoring
- Persistent data volumes

**Development Mode:**
- Live code reloading
- Debug logging enabled
- SQLite browser available at `:8080`
- Source code mounted as volume

## 📊 Monitoring & Logs

### View Logs
```powershell
.\deploy.ps1 logs
```

### Check Service Status
```powershell
.\deploy.ps1 status
```

### Health Monitoring
The system includes comprehensive health checks:
- Database connectivity
- Scheduler status
- Data file freshness
- Service responsiveness

## 🔧 Troubleshooting

### Common Issues

**Docker not found:**
```
Solution: Install Docker Desktop and ensure it's running
```

**Port 5001 already in use:**
```
Solution: Stop other services or change port in docker-compose.yml
```

**Services not starting:**
```
Solution: Check logs with .\deploy.ps1 logs
```

**Database empty:**
```
Solution: Run manual scraping with .\deploy.ps1 scrape
```

### Debugging Steps

1. **Check Docker status:**
   ```powershell
   docker --version
   docker info
   ```

2. **View service logs:**
   ```powershell
   .\deploy.ps1 logs
   ```

3. **Check health endpoints:**
   ```powershell
   curl http://localhost:5001/health
   ```

4. **Inspect containers:**
   ```powershell
   docker-compose ps
   docker-compose exec api-server bash
   ```

## 🚀 Deployment Options

### Local Development
```powershell
.\deploy.ps1 dev
```

### Production (Local)
```powershell
.\deploy.ps1 prod
```

### Cloud Deployment
For cloud deployment, use the included `k8s-deployment.yaml` or `aws-cloudformation.yaml` files.

## 📈 Scaling

### Horizontal Scaling
```yaml
# In docker-compose.yml
api-server:
  # ... existing config ...
  deploy:
    replicas: 3
```

### Load Balancing
Add nginx or traefik as reverse proxy for multiple API instances.

## 🔒 Security Considerations

- Services run as non-root user
- Network isolation with custom bridge
- Health checks prevent unhealthy containers
- Persistent volumes for data safety

## 🆚 SLURM vs Docker Comparison

| Feature | SLURM | Docker |
|---------|-------|--------|
| **Setup** | Complex cluster setup | Simple desktop install |
| **Development** | Cluster-only testing | Local development |
| **Scaling** | Manual job submission | Automatic container management |
| **Monitoring** | Basic SLURM logs | Rich health checks & metrics |
| **Networking** | Limited | Full networking stack |
| **Portability** | Cluster-specific | Runs anywhere |

## 📝 Migration Notes

### From SLURM to Docker

Your original SLURM files are preserved but no longer needed:
- `*.slurm` files → `docker-compose.yml`
- Manual job submission → Automatic scheduling
- Cluster resources → Container resources
- SLURM logs → Docker logs + health endpoints

### Data Compatibility
- Existing SQLite database: ✅ Compatible
- Text output files: ✅ Compatible  
- Configuration: ✅ Enhanced with environment variables

## 🎯 Next Steps

1. **Start with development deployment** to test locally
2. **Monitor health endpoints** to ensure everything works
3. **Set up cloud deployment** for production use
4. **Implement star schema** for analytics (next phase)
5. **Add alerting** for production monitoring

## 🆘 Support

For issues:
1. Check the troubleshooting section above
2. Review service logs: `.\deploy.ps1 logs`
3. Check health status: `.\deploy.ps1 status`
4. Ensure Docker Desktop is running