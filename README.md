# 📺 TV Program Web Scraper

An automated TV program scraping system with real-time viewer simulation and global API deployment.

## 🚀 Live Demo
- **Global API**: https://tv-scraper.tvdata.workers.dev
- **Local API**: http://localhost:5001 (when running locally)
- **Endpoints**: `/status`, `/now-playing`, `/viewers`

> 🔄 **API Sync**: Both local and global APIs serve identical real TV data formats

## 🎯 Project Overview

This project demonstrates a complete data pipeline from web scraping to global API deployment:

```
🕷️ Scrapers → 🗄️ Database → 🖥️ Local API → 🌍 Global Deployment
```

### **Core Features:**
- ✅ **Automated scraping** of 3 TV channels (BBC Earth, Discovery, National Geographic)
- ✅ **SQLite database** with structured TV program data
- ✅ **Real-time viewer simulation** with realistic counts
- ✅ **Local development** environment with Docker
- ✅ **Global deployment** on Cloudflare Workers edge network
- ✅ **Scheduled automation** every 6 hours

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Scraping** | Python + BeautifulSoup |
| **Database** | SQLite |
| **Local API** | Flask |
| **Containerization** | Docker + Docker Compose |
| **Global API** | Cloudflare Workers (Serverless) |
| **Automation** | Python Schedule |
| **Deployment** | Git + Wrangler CLI |

## 📂 Project Structure

```
tv-scraper/
├── 🕷️ scrapers/
│   ├── scraper_BBC.py          # BBC Earth scraper
│   ├── scraper_Disc.py         # Discovery Channel scraper
│   └── scraper_NatGeo.py       # National Geographic scraper
├── 🗄️ data/
│   ├── tvguide.db              # SQLite database
│   ├── tv_programs_BBC.txt     # Raw scraped data
│   ├── tv_programs_Disc.txt
│   └── tv_programs_NatGeo.txt
├── 🖥️ local-api/
│   ├── flask_now_playing.py    # Local Flask API server
│   ├── load_tv_programs_sqlite.py # Database loader
│   └── scheduler.py            # Automated scraping scheduler
├── 🌍 global-api/
│   ├── worker.js               # Cloudflare Workers API
│   └── wrangler.toml           # Cloudflare configuration
└── 🐳 deployment/
    ├── docker-compose.yml      # Local environment
    ├── Dockerfile              # Container definition
    └── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### **Option 1: Local Development**
```bash
# Clone the repository
git clone https://github.com/sarontebebe7/tv-scraper.git
cd tv-scraper

# Start with Docker (recommended)
docker-compose up -d

# Access local API
curl http://localhost:5001/now-playing
```

### **Option 2: Use Global API**
```bash
# Already deployed and running!
curl https://tv-scraper.tvdata.workers.dev/now-playing
```

## � API Synchronization

Both local and global APIs now serve **identical real TV data**:

| Environment | URL | Data Source |
|-------------|-----|-------------|
| **Local Development** | `http://localhost:5001` | Real scraped data from SQLite |
| **Global Production** | `https://tv-scraper.tvdata.workers.dev` | Real data (synchronized) |

### **Why This Matters for Teams:**
- ✅ **Consistent Integration**: Same JSON format across environments  
- ✅ **Real Data**: No demo/mock data - actual Slovak TV programming
- ✅ **Reliable Testing**: Develop locally, deploy globally with confidence
- ✅ **Live Data**: Current programs updated every 6 hours

## �📊 API Endpoints

### **GET /status**
System health and configuration information
```json
{
  "service": "TV Program Scraper API",
  "status": "operational",
  "timestamp": "2025-11-06T10:15:00.000Z",
  "stats": {
    "database": "connected",
    "channels": ["BBC Earth", "Discovery Channel", "National Geographic"]
  }
}
```

### **GET /now-playing**  
Current TV programs across all channels (REAL DATA)
```json
[
  {
    "channel": "BBC Earth",
    "title": "Život, smrt a odkaz Tutanchamona 1",
    "start": "09:10:00",
    "date": "06.11.2025",
    "csfd_id": ""
  },
  {
    "channel": "Discovery Channel", 
    "title": "Lovci odpadu 12",
    "start": "09:00:00",
    "date": "06.11.2025",
    "csfd_id": ""
  }
]
```

### **GET /viewers**
Live viewer counts simulation
```json
[
  {
    "channel": "Discovery Channel",
    "viewers": "4185"
  },
  {
    "channel": "BBC Earth", 
    "viewers": "3925"
  },
  {
    "channel": "National Geographic",
    "viewers": "4431"
  }
]
  "success": true,
  "data": [
    {
      "channel": "BBC Earth",
      "viewers": "4,245",
      "trend": "↗",
      "region_breakdown": {
        "North America": 1698,
        "Europe": 1486,
        "Asia": 637
      }
    }
  ]
}
```

## 🔄 Automated Data Pipeline

The system automatically:

1. **Scrapes** TV program data every 6 hours
2. **Processes** and cleans the data
3. **Updates** SQLite database
4. **Logs** all operations with status monitoring
5. **Serves** data via both local and global APIs

```python
# Automation powered by scheduler.py
schedule.every(6).hours.do(run_all_scrapers)
schedule.every().day.at("06:00").do(run_all_scrapers)
```

## 🌍 Deployment Architecture

### **Local Environment:**
- **Docker Compose** for easy development
- **Flask API** with full database access
- **Complete feature set** for testing

### **Production Environment:**
- **Cloudflare Workers** for global edge deployment
- **Automatic scaling** and 99.9% uptime
- **Global CDN** for fast worldwide access

## 📈 Future Enhancements

- [ ] **Star Schema** implementation for advanced analytics
- [ ] **Real-time data streaming** with WebSockets
- [ ] **Machine learning** for viewer prediction
- [ ] **Multi-language support** for international channels
- [ ] **GraphQL API** for flexible data queries

## 🤝 Contributing

This project demonstrates modern data engineering practices including:
- Web scraping at scale
- Database design and management
- API development and deployment
- Container orchestration
- Global edge computing
- Automated data pipelines

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🎯 About

Created as a demonstration of end-to-end data pipeline development, from web scraping to global API deployment using modern cloud infrastructure.

**Live API**: https://tv-scraper.tvdata.workers.dev