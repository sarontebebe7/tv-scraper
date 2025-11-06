# TV Scraper - Dual Deployment Setup

## 🚀 Production (Cloudflare Workers)
**Live URL**: https://tv-scraper.tvdata.workers.dev

### Features:
- ✅ **Global CDN** (200+ locations worldwide)
- ✅ **Auto-scaling** (handles any traffic)
- ✅ **100% Free** (100K requests/day)
- ✅ **Instant deployments**
- ✅ **HTTPS included**

### Endpoints:
- `GET /status` - API health and info
- `GET /now-playing` - Current TV programs  
- `GET /viewers` - Live viewer counts

---

## 🛠️ Local Development (Flask + Docker)

### Start Local Environment:
```bash
# Start with Docker (recommended)
docker-compose up -d

# OR start manually
python flask_now_playing.py
```

### Local URLs:
- http://localhost:5001/status
- http://localhost:5001/now-playing
- http://localhost:5001/viewers

---

## 📂 Project Structure

```
├── worker.js              # 🌍 Cloudflare Workers (Production)
├── wrangler.toml           # ⚙️ Cloudflare configuration
├── flask_now_playing.py    # 🐍 Flask app (Local development)
├── docker-compose.yml      # 🐳 Local Docker setup
├── requirements.txt        # 📦 Python dependencies
├── tvguide.db             # 💾 Local SQLite database
└── scrapers/              # 🔍 Data collection scripts
```

---

## 🔄 Development Workflow

### 1. **Develop Locally**
```bash
# Start local environment
docker-compose up -d

# Test changes at localhost:5001
curl http://localhost:5001/now-playing
```

### 2. **Deploy to Production**
```bash
# Deploy to Cloudflare Workers
wrangler deploy

# Test production
curl https://tv-scraper.tvdata.workers.dev/now-playing
```

---

## 🎯 When to Use Each

### **Local Development (Flask + Docker)**
- ✅ **Testing new features**
- ✅ **Database development**
- ✅ **Debugging complex logic**
- ✅ **Full feature testing**

### **Production (Cloudflare Workers)**
- ✅ **Live API for users**
- ✅ **Portfolio demonstrations**
- ✅ **Mobile app backends**
- ✅ **Public sharing**

---

## 📊 Performance Comparison

| Feature | Local (Docker) | Production (Cloudflare) |
|---------|----------------|-------------------------|
| **Speed** | Fast (local) | Faster (global edge) |
| **Database** | Full SQLite | Simulated data |
| **Features** | Complete | API optimized |
| **Cost** | Free | Free |
| **Uptime** | When PC on | 99.9% guaranteed |

---

## 🚀 Quick Commands

### Local Development:
```bash
docker-compose up -d          # Start local environment
docker-compose logs -f        # View logs
docker-compose down           # Stop environment
```

### Production Deployment:
```bash
wrangler deploy               # Deploy to Cloudflare
wrangler tail                 # View live logs
wrangler dev                  # Local Cloudflare testing
```

---

## 🎉 Best of Both Worlds!

- **Develop locally** with full database and features
- **Deploy globally** with Cloudflare's edge network
- **Test locally** before production deployment
- **Scale infinitely** with Cloudflare Workers

Your TV Scraper now has a **professional development and deployment pipeline**! 🌍