# Student Credits Application Helper
# Run this to get direct links and track your applications

Write-Host "🎓 STUDENT CREDITS APPLICATION HELPER" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

function Show-StudentPackBenefits {
    Write-Host ""
    Write-Host "💰 GitHub Student Developer Pack Benefits:" -ForegroundColor Yellow
    Write-Host "- $200 DigitalOcean Credits (24 months)" -ForegroundColor White
    Write-Host "- $100 AWS Credits (12 months)" -ForegroundColor White
    Write-Host "- $100 Azure Credits (12 months)" -ForegroundColor White
    Write-Host "- $300 Google Cloud Credits (3 months)" -ForegroundColor White
    Write-Host "- Free .me domain (1 year)" -ForegroundColor White
    Write-Host "- GitHub Pro (free while student)" -ForegroundColor White
    Write-Host "- JetBrains IDEs (all free)" -ForegroundColor White
    Write-Host "- And 100+ more developer tools!" -ForegroundColor White
    Write-Host ""
    Write-Host "Total Value: $1000+ in free credits and tools!" -ForegroundColor Cyan
}

function Show-ApplicationLinks {
    Write-Host ""
    Write-Host "🚀 APPLY NOW - Direct Links:" -ForegroundColor Yellow
    Write-Host "1. GitHub Student Pack (MAIN): https://education.github.com/pack" -ForegroundColor White
    Write-Host "2. AWS Educate: https://aws.amazon.com/education/awseducate/" -ForegroundColor White
    Write-Host "3. Google Cloud Education: https://cloud.google.com/edu" -ForegroundColor White
    Write-Host "4. Azure Students: https://azure.microsoft.com/free/students/" -ForegroundColor White
    Write-Host ""
    Write-Host "⭐ START WITH #1 - It includes most others!" -ForegroundColor Cyan
}

function Show-RequiredDocuments {
    Write-Host ""
    Write-Host "📋 What You Need to Apply:" -ForegroundColor Yellow
    Write-Host "Option 1: Student email (.edu domain)" -ForegroundColor White
    Write-Host "Option 2: Student ID card (take a photo)" -ForegroundColor White
    Write-Host "Option 3: Enrollment verification letter" -ForegroundColor White
    Write-Host "Option 4: Recent transcript" -ForegroundColor White
    Write-Host ""
    Write-Host "✅ Any ONE of these is enough!" -ForegroundColor Green
}

function Show-EligibilityCheck {
    Write-Host ""
    Write-Host "🎯 Are You Eligible? (Check all that apply)" -ForegroundColor Yellow
    Write-Host "[ ] University/College student" -ForegroundColor White
    Write-Host "[ ] High school student (13+)" -ForegroundColor White
    Write-Host "[ ] Bootcamp student" -ForegroundColor White
    Write-Host "[ ] Online course student (Coursera, edX, etc.)" -ForegroundColor White
    Write-Host "[ ] Homeschool student" -ForegroundColor White
    Write-Host ""
    Write-Host "If you checked ANY box, you likely qualify!" -ForegroundColor Green
}

function Show-ApplicationSteps {
    Write-Host ""
    Write-Host "📝 Step-by-Step Application Process:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://education.github.com/pack" -ForegroundColor White
    Write-Host "2. Click 'Get Student Benefits'" -ForegroundColor White
    Write-Host "3. Sign in with GitHub (create account if needed)" -ForegroundColor White
    Write-Host "4. Fill out the form with your school info" -ForegroundColor White
    Write-Host "5. Upload verification document (photo/scan)" -ForegroundColor White
    Write-Host "6. Submit and wait 1-7 days for approval" -ForegroundColor White
    Write-Host "7. Get email confirmation and activate benefits!" -ForegroundColor White
    Write-Host ""
    Write-Host "⏰ Total time: 5-10 minutes to apply" -ForegroundColor Cyan
}

function Show-TVScraperBenefit {
    Write-Host ""
    Write-Host "🎯 Perfect for Your TV Scraper Project:" -ForegroundColor Yellow
    Write-Host "Current Plan: Railway (Free)" -ForegroundColor White
    Write-Host "With Student Credits: DigitalOcean ($200 = 50 months free!)" -ForegroundColor Green
    Write-Host "Plus: Learn AWS, Azure, Google Cloud for future projects" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Strategy:" -ForegroundColor Blue
    Write-Host "1. Deploy TV Scraper on Railway now (free)" -ForegroundColor White
    Write-Host "2. Apply for student credits today" -ForegroundColor White
    Write-Host "3. Use credits for advanced features and learning" -ForegroundColor White
}

function Create-ApplicationTracker {
    Write-Host ""
    Write-Host "📋 Creating Application Tracker..." -ForegroundColor Blue
    
    $trackerContent = @"
# Student Credits Application Tracker

## Application Status
- [ ] GitHub Student Pack Applied: ___________
- [ ] Verification Document Uploaded: ___________
- [ ] Approval Received: ___________
- [ ] Benefits Activated: ___________

## Credits Available
- [ ] DigitalOcean: $200 (24 months) - Activated: _____
- [ ] AWS: $100 (12 months) - Activated: _____
- [ ] Azure: $100 (12 months) - Activated: _____
- [ ] Google Cloud: $300 (3 months) - Activated: _____

## Current Projects
- [x] TV Scraper: Deployed on Railway (FREE)
- [ ] Next project: ___________
- [ ] Learning project: ___________

## Monthly Usage Tracking
Month 1: $_____ spent, $_____ remaining
Month 2: $_____ spent, $_____ remaining
Month 3: $_____ spent, $_____ remaining

## Notes
- Application submitted: ___________
- Expected approval: ___________
- Backup plan: Continue with Railway free tier
"@

    $trackerContent | Out-File -FilePath "student-credits-tracker.md" -Encoding UTF8
    Write-Host "✅ Created: student-credits-tracker.md" -ForegroundColor Green
    Write-Host "Use this file to track your application progress!" -ForegroundColor White
}

function Open-ApplicationPage {
    Write-Host ""
    Write-Host "🚀 Opening GitHub Student Pack application page..." -ForegroundColor Blue
    
    try {
        Start-Process "https://education.github.com/pack"
        Write-Host "✅ Application page opened in your browser!" -ForegroundColor Green
        Write-Host "Follow the steps above to complete your application." -ForegroundColor White
    } catch {
        Write-Host "❌ Could not open browser automatically." -ForegroundColor Red
        Write-Host "Please manually go to: https://education.github.com/pack" -ForegroundColor Yellow
    }
}

# Main execution
Show-StudentPackBenefits
Show-EligibilityCheck
Show-RequiredDocuments
Show-ApplicationSteps
Show-ApplicationLinks
Show-TVScraperBenefit
Create-ApplicationTracker

Write-Host ""
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Apply for GitHub Student Pack now (5 minutes)" -ForegroundColor White
Write-Host "2. Continue with Railway deployment (your project works free!)" -ForegroundColor White
Write-Host "3. Use tracker file to monitor your application" -ForegroundColor White

$response = Read-Host "`nWould you like me to open the GitHub Student Pack application page? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y' -or $response -eq 'yes') {
    Open-ApplicationPage
} else {
    Write-Host ""
    Write-Host "No problem! Remember to apply at: https://education.github.com/pack" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎉 Good luck with your application!" -ForegroundColor Green
Write-Host "💡 Your TV Scraper is ready to deploy for FREE regardless!" -ForegroundColor Cyan