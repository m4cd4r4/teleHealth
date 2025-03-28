# PowerShell script to run the TeleHealth application locally without Docker

Write-Host "TeleHealth Local Development Runner" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Create and activate virtual environment
if (-not (Test-Path ".\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if (-not $?) {
        Write-Host "Failed to create virtual environment. Make sure Python is installed." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies for each service
Write-Host "Installing dependencies for gateway..." -ForegroundColor Yellow
pip install -r gateway/requirements.txt

Write-Host "Installing dependencies for auth-service..." -ForegroundColor Yellow
pip install -r auth-service/requirements.txt

Write-Host "Installing dependencies for patient-service..." -ForegroundColor Yellow
pip install -r patient-service/requirements.txt

Write-Host ""
Write-Host "Dependencies installed successfully." -ForegroundColor Green
Write-Host ""

# Check if PostgreSQL is installed
$pgInstalled = $false
try {
    $pgVersion = Invoke-Expression "psql --version" 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pgInstalled = $true
        Write-Host "PostgreSQL is installed: $pgVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "PostgreSQL is not installed or not in PATH." -ForegroundColor Yellow
}

if (-not $pgInstalled) {
    Write-Host "Warning: PostgreSQL is required for the auth and patient services." -ForegroundColor Yellow
    Write-Host "Please install PostgreSQL from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    Write-Host ""
}

# Check if Redis is installed
$redisInstalled = $false
try {
    $redisVersion = Invoke-Expression "redis-cli --version" 2>&1
    if ($LASTEXITCODE -eq 0) {
        $redisInstalled = $true
        Write-Host "Redis is installed: $redisVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "Redis is not installed or not in PATH." -ForegroundColor Yellow
}

if (-not $redisInstalled) {
    Write-Host "Warning: Redis is required for rate limiting and caching in the gateway." -ForegroundColor Yellow
    Write-Host "Please install Redis for Windows from: https://github.com/tporadowski/redis/releases" -ForegroundColor Yellow
    Write-Host ""
}

# Instructions for running the services
Write-Host "To run the TeleHealth services, open three separate terminal windows:" -ForegroundColor Cyan
Write-Host ""

Write-Host "Terminal 1 - Auth Service:" -ForegroundColor White
Write-Host "cd $((Get-Location).Path)\auth-service" -ForegroundColor White
Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "uvicorn src.main:app --reload --port 8001" -ForegroundColor White
Write-Host ""

Write-Host "Terminal 2 - Patient Service:" -ForegroundColor White
Write-Host "cd $((Get-Location).Path)\patient-service" -ForegroundColor White
Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "uvicorn src.main:app --reload --port 8002" -ForegroundColor White
Write-Host ""

Write-Host "Terminal 3 - API Gateway:" -ForegroundColor White
Write-Host "cd $((Get-Location).Path)\gateway" -ForegroundColor White
Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "uvicorn src.main:app --reload --port 8000" -ForegroundColor White
Write-Host ""

Write-Host "After starting all services, you can access the application at:" -ForegroundColor Cyan
Write-Host "- API Gateway: http://localhost:8000" -ForegroundColor White
Write-Host "- API Documentation: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""

# Ask which service to run in this terminal
Write-Host "Would you like to run one of the services in this terminal?" -ForegroundColor Cyan
Write-Host "1. Auth Service (port 8001)" -ForegroundColor White
Write-Host "2. Patient Service (port 8002)" -ForegroundColor White
Write-Host "3. API Gateway (port 8000)" -ForegroundColor White
Write-Host "4. None (exit script)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host "Starting Auth Service..." -ForegroundColor Yellow
        Set-Location -Path "$((Get-Location).Path)\auth-service"
        uvicorn src.main:app --reload --port 8001
    }
    "2" {
        Write-Host "Starting Patient Service..." -ForegroundColor Yellow
        Set-Location -Path "$((Get-Location).Path)\patient-service"
        uvicorn src.main:app --reload --port 8002
    }
    "3" {
        Write-Host "Starting API Gateway..." -ForegroundColor Yellow
        Set-Location -Path "$((Get-Location).Path)\gateway"
        uvicorn src.main:app --reload --port 8000
    }
    "4" {
        Write-Host "Exiting script." -ForegroundColor Yellow
    }
    default {
        Write-Host "Invalid choice. Exiting script." -ForegroundColor Red
    }
}
