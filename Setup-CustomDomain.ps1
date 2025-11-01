# PowerShell Script to Add EduHelm Custom Domain
# Must run as Administrator!

$hostsPath = "C:\Windows\System32\drivers\etc\hosts"

Write-Host "`n🔧 EduHelm Custom Domain Setup" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ ERROR: This script must run as Administrator!`n" -ForegroundColor Red
    Write-Host "How to run as Administrator:" -ForegroundColor Yellow
    Write-Host "1. Right-click on this script" -ForegroundColor White
    Write-Host "2. Select 'Run as Administrator'`n" -ForegroundColor White
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# Read current hosts file
$hostsContent = Get-Content $hostsPath

# Check if already exists
$alreadyExists = $hostsContent | Where-Object { $_ -match "eduhelm.local" }

if ($alreadyExists) {
    Write-Host "✅ EduHelm domain already configured!`n" -ForegroundColor Green
} else {
    # Add entries
    Write-Host "Adding custom domain to Windows hosts file..." -ForegroundColor Yellow
    
    $newEntries = @"

# EduHelm Educational Platform - Custom Domain
127.0.0.1       eduhelm.local
127.0.0.1       www.eduhelm.local
"@
    
    Add-Content -Path $hostsPath -Value $newEntries
    Write-Host "✅ Successfully added eduhelm.local to hosts file!`n" -ForegroundColor Green
}

Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "`nYou can now access EduHelm at:" -ForegroundColor Cyan
Write-Host "   http://eduhelm.local:8000" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host "   http://www.eduhelm.local:8000`n" -ForegroundColor White -BackgroundColor DarkBlue

Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Start your Django server" -ForegroundColor White
Write-Host "2. Open browser and go to: http://eduhelm.local:8000" -ForegroundColor White
Write-Host "3. Bookmark it for easy access!`n" -ForegroundColor White

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
