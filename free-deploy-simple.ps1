# Free Deployment Guide for TV Scraper
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("railway", "render", "fly")]
    [string]$Platform = "railway"
)

Write-Host "FREE TV Scraper Deployment" -ForegroundColor Green
Write-Host "==========================" -ForegroundColor Green

function Show-FreeOptions {
    Write-Host ""
    Write-Host "Best FREE Deployment Options:" -ForegroundColor Yellow
    Write-Host "1. Railway - 500 hours/month, PostgreSQL included" -ForegroundColor White
    Write-Host "2. Render - 750 hours/month, sleeps after 15min" -ForegroundColor White  
    Write-Host "3. Fly.io - 3 small VMs, 3GB storage" -ForegroundColor White
    Write-Host ""
    Write-Host "All options are completely FREE for your project!" -ForegroundColor Cyan
}

function Deploy-Railway {
    Write-Host ""
    Write-Host "Railway Deployment (RECOMMENDED)" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    
    Write-Host "Why Railway is perfect:" -ForegroundColor Blue
    Write-Host "- Completely FREE for 500 hours/month" -ForegroundColor White
    Write-Host "- No sleep mode" -ForegroundColor White
    Write-Host "- Built-in PostgreSQL database" -ForegroundColor White
    Write-Host "- One-click GitHub deployment" -ForegroundColor White
    
    Write-Host ""
    Write-Host "Step-by-step deployment:" -ForegroundColor Yellow
    Write-Host "1. Go to https://railway.app" -ForegroundColor White
    Write-Host "2. Sign up with GitHub" -ForegroundColor White
    Write-Host "3. Click 'New Project' > 'Deploy from GitHub repo'" -ForegroundColor White
    Write-Host "4. Select your tv-scraper repository" -ForegroundColor White
    Write-Host "5. Add PostgreSQL database service" -ForegroundColor White
    Write-Host "6. Your app will be live at: yourapp.up.railway.app" -ForegroundColor White
}

function Deploy-Render {
    Write-Host ""
    Write-Host "Render Deployment" -ForegroundColor Green
    Write-Host "=================" -ForegroundColor Green
    
    Write-Host "Render setup:" -ForegroundColor Yellow
    Write-Host "1. Go to https://render.com" -ForegroundColor White
    Write-Host "2. Connect your GitHub account" -ForegroundColor White
    Write-Host "3. Create new Web Service" -ForegroundColor White
    Write-Host "4. Build Command: pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host "5. Start Command: python flask_now_playing.py" -ForegroundColor Yellow
}

function Check-GitSetup {
    Write-Host ""
    Write-Host "Git Repository Setup" -ForegroundColor Blue
    Write-Host "====================" -ForegroundColor Blue
    
    if (Test-Path ".git") {
        Write-Host "Git repository already initialized" -ForegroundColor Green
    } else {
        Write-Host "Initialize Git repository:" -ForegroundColor Yellow
        Write-Host "git init" -ForegroundColor White
        Write-Host "git add ." -ForegroundColor White
        Write-Host "git commit -m 'Initial commit'" -ForegroundColor White
        Write-Host "git remote add origin https://github.com/yourusername/tv-scraper.git" -ForegroundColor White
        Write-Host "git push -u origin main" -ForegroundColor White
    }
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
    default {
        Deploy-Railway
    }
}

Write-Host ""
Write-Host "RECOMMENDED: Railway" -ForegroundColor Green
Write-Host "- Most reliable free option" -ForegroundColor White
Write-Host "- No sleep mode" -ForegroundColor White
Write-Host "- Perfect for your project" -ForegroundColor White

Write-Host ""
Write-Host "Ready to deploy for FREE!" -ForegroundColor Cyan
Write-Host "Go to: https://railway.app" -ForegroundColor Yellow