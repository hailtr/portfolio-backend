# PowerShell script to start the development server
# Usage: .\scripts\start_dev.ps1

Write-Host "Starting Portfolio Backend..." -ForegroundColor Cyan

# Navigate to project root
Set-Location -Path (Split-Path -Parent $PSScriptRoot)

# Check if venv exists
if (-Not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created!" -ForegroundColor Green
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Write-Host "Dependencies installed!" -ForegroundColor Green
} else {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    .\venv\Scripts\Activate.ps1
}

# Check if .env exists
if (-Not (Test-Path ".\.env")) {
    Write-Host "Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Copy env.example to .env and configure your settings." -ForegroundColor Yellow
    Write-Host ""
}

# Start the application
Write-Host "Starting Flask server..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

python run.py


