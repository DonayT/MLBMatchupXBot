Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    MLB Lineup Bot - Continuous Runner" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting MLB Lineup Bot..." -ForegroundColor Green
Write-Host "Will run every 15 minutes" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Red
Write-Host "Will auto-stop when all games are processed" -ForegroundColor Magenta
Write-Host ""

while ($true) {
    Write-Host ""
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Running MLB script..." -ForegroundColor Cyan
    
    try {
        $result = python ..\src\MLBMatchup.py
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 42) {
            Write-Host "All games processed! Stopping bot..." -ForegroundColor Green
            Write-Host "Bot will restart tomorrow for new games" -ForegroundColor Yellow
            break
        } else {
            Write-Host "Script completed successfully" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "Script failed: $_" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Waiting 15 minutes until next run..." -ForegroundColor Yellow
    Write-Host "(Press Ctrl+C to stop)" -ForegroundColor Gray
    
    Start-Sleep -Seconds 900
}

Write-Host ""
Write-Host "Bot stopped - all games processed for today!" -ForegroundColor Green
Write-Host "Run again tomorrow for new games" -ForegroundColor Green 