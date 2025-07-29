Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    MLB Lineup Bot - Continuous Runner" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Starting MLB Lineup Bot..." -ForegroundColor Green
Write-Host "⏰ Will run every 15 minutes" -ForegroundColor Yellow
Write-Host "🛑 Press Ctrl+C to stop" -ForegroundColor Red
Write-Host ""

while ($true) {
    Write-Host ""
    Write-Host "🕐 [$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Running MLB script..." -ForegroundColor Cyan
    
    try {
        python ..\src\MLBMatchup.py
        Write-Host "✅ Script completed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Script failed: $_" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "⏳ Waiting 15 minutes until next run..." -ForegroundColor Yellow
    Write-Host "(Press Ctrl+C to stop)" -ForegroundColor Gray
    
    Start-Sleep -Seconds 900
} 