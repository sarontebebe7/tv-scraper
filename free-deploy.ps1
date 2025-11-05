# Free Deployment Script for TV Scraper
# Usage: .\free-deploy.ps1 -Platform railway

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("railway", "render", "fly", "vercel")]
    [string]$Platform = "railway"
)

Write-Host "🆓 FREE TV Scraper Deployment" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

function Show-FreeOptions {
    Write-Host ""
    Write-Host "🎯 Best FREE Deployment Options:" -ForegroundColor Yellow
    Write-Host "1. Railway - 500 hours/month, PostgreSQL included, no sleep" -ForegroundColor White
    Write-Host "2. Render - 750 hours/month, sleeps after 15min" -ForegroundColor White  
    Write-Host "3. Fly.io - 3 small VMs, 3GB storage" -ForegroundColor White
    Write-Host "4. Vercel - Unlimited (serverless functions only)" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 All options are completely FREE for your project size!" -ForegroundColor Cyan
}

function Deploy-Railway {
    Write-Host ""
    Write-Host "🚂 Railway Deployment (RECOMMENDED)" -ForegroundColor Green
    Write-Host "====================================" -ForegroundColor Green
    
    Write-Host "✅ Why Railway is perfect for your project:" -ForegroundColor Blue
    Write-Host "• Completely FREE for 500 hours/month" -ForegroundColor White
    Write-Host "• No sleep mode (unlike Heroku)" -ForegroundColor White
    Write-Host "• Built-in PostgreSQL database" -ForegroundColor White
    Write-Host "• One-click GitHub deployment" -ForegroundColor White
    Write-Host "• Custom domain support" -ForegroundColor White
    
    Write-Host ""
    Write-Host "📋 Step-by-step deployment:" -ForegroundColor Yellow
    Write-Host "1. Go to https://railway.app" -ForegroundColor White
    Write-Host "2. Sign up with GitHub" -ForegroundColor White
    Write-Host "3. Click 'New Project' > 'Deploy from GitHub repo'" -ForegroundColor White
    Write-Host "4. Select your tv-scraper repository" -ForegroundColor White
    Write-Host "5. Add PostgreSQL database service" -ForegroundColor White
    Write-Host "6. Your app will be live at: yourapp.up.railway.app" -ForegroundColor White
    
    Write-Host ""
    Write-Host "🔧 Files ready for Railway:" -ForegroundColor Blue
    Write-Host "• Dockerfile.railway - Optimized container" -ForegroundColor Green
    Write-Host "• railway.toml - Railway configuration" -ForegroundColor Green
    Write-Host "• requirements.txt - Python dependencies" -ForegroundColor Green
}

function Deploy-Render {
    Write-Host ""
    Write-Host "🎨 Render Deployment" -ForegroundColor Green
    Write-Host "====================" -ForegroundColor Green
    
    Write-Host "📋 Render setup:" -ForegroundColor Yellow
    Write-Host "1. Go to https://render.com" -ForegroundColor White
    Write-Host "2. Connect your GitHub account" -ForegroundColor White
    Write-Host "3. Create new Web Service" -ForegroundColor White
    Write-Host "4. Select your repository" -ForegroundColor White
    Write-Host "5. Use these settings:" -ForegroundColor White
    Write-Host "   • Build Command: pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host "   • Start Command: python flask_now_playing.py" -ForegroundColor Yellow
    Write-Host "   • Environment: Python 3" -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "⚠️ Note: Render sleeps after 15 minutes of inactivity" -ForegroundColor Yellow
}

function Deploy-Fly {
    Write-Host ""
    Write-Host "🪰 Fly.io Deployment" -ForegroundColor Green
    Write-Host "====================" -ForegroundColor Green
    
    Write-Host "📋 Fly.io setup:" -ForegroundColor Yellow
    Write-Host "1. Install flyctl:" -ForegroundColor White
    Write-Host "   iwr https://fly.io/install.ps1 -useb | iex" -ForegroundColor Yellow
    Write-Host "2. Create account: flyctl auth signup" -ForegroundColor White
    Write-Host "3. Launch app: flyctl launch" -ForegroundColor White
    Write-Host "4. Deploy: flyctl deploy" -ForegroundColor White
    
    Write-Host ""
    Write-Host "💡 Fly.io offers 3 free VMs with 3GB storage" -ForegroundColor Cyan
}

function Deploy-Vercel {
    Write-Host ""
    Write-Host "▲ Vercel Deployment (Serverless)" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    
    Write-Host "📋 Vercel setup (requires code changes):" -ForegroundColor Yellow
    Write-Host "1. Convert Flask to serverless functions" -ForegroundColor White
    Write-Host "2. Use external database (Supabase)" -ForegroundColor White
    Write-Host "3. Deploy via: vercel --prod" -ForegroundColor White
    
    Write-Host ""
    Write-Host "⚠️ Requires refactoring for serverless architecture" -ForegroundColor Yellow
}

function Check-GitSetup {
    Write-Host ""
    Write-Host "📦 Git Repository Setup" -ForegroundColor Blue
    Write-Host "=======================" -ForegroundColor Blue
    
    if (Test-Path ".git") {
        Write-Host "✅ Git repository already initialized" -ForegroundColor Green
        
        try {
            $remote = git remote get-url origin 2>$null
            Write-Host "✅ Remote origin: $remote" -ForegroundColor Green
        } catch {
            Write-Host "⚠️ No remote origin set. Add one with:" -ForegroundColor Yellow
            Write-Host "git remote add origin https://github.com/yourusername/tv-scraper.git" -ForegroundColor White
        }
    } else {
        Write-Host "📋 Initialize Git repository:" -ForegroundColor Yellow
        Write-Host "git init" -ForegroundColor White
        Write-Host "git add ." -ForegroundColor White
        Write-Host "git commit -m 'Initial commit'" -ForegroundColor White
        Write-Host "git remote add origin https://github.com/yourusername/tv-scraper.git" -ForegroundColor White
        Write-Host "git push -u origin main" -ForegroundColor White
    }
}

function Show-StudentCredits {
    Write-Host ""
    Write-Host "🎓 FREE Student Credits Available" -ForegroundColor Cyan
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host "If you're a student, get these FREE credits:" -ForegroundColor Yellow
    Write-Host "• GitHub Student Pack: https://education.github.com/pack" -ForegroundColor White
    Write-Host "  - $200 DigitalOcean credits" -ForegroundColor Green
    Write-Host "  - $100 AWS credits" -ForegroundColor Green
    Write-Host "  - Free Azure credits" -ForegroundColor Green
    Write-Host "  - Free Google Cloud credits" -ForegroundColor Green
    Write-Host ""
    Write-Host "• AWS Free Tier: 12 months free services" -ForegroundColor White
    Write-Host "• Google Cloud: $300 credits for new users" -ForegroundColor White
    Write-Host "• Azure: $200 credits for students" -ForegroundColor White
}

# Main execution
Show-FreeOptions
Check-GitSetup

switch ($Platform) {
    "railway" {
        Deploy-Railway
    }
    "render" {
        Deploy-Render
    }
    "fly" {
        Deploy-Fly
    }
    "vercel" {
        Deploy-Vercel
    }
}

Show-StudentCredits

Write-Host ""
Write-Host "🎯 RECOMMENDED: Railway" -ForegroundColor Green
Write-Host "• Most reliable free option" -ForegroundColor White
Write-Host "• No sleep mode" -ForegroundColor White
Write-Host "• PostgreSQL included" -ForegroundColor White
Write-Host "• Perfect for your project" -ForegroundColor White

Write-Host ""
Write-Host "🚀 Ready to deploy for FREE!" -ForegroundColor Cyan
Write-Host "Choose Railway at: https://railway.app" -ForegroundColor Yellow