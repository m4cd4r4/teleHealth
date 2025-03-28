# PowerShell script to run the TeleHealth application

Write-Host "TeleHealth Application Runner" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
$dockerRunning = $false
try {
    $dockerStatus = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        $dockerRunning = $true
        Write-Host "Docker is running." -ForegroundColor Green
    } else {
        Write-Host "Docker is not running." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Docker is not installed or not running." -ForegroundColor Yellow
}

# Check if .env files exist, create from examples if they don't
$services = @("gateway", "auth-service", "patient-service")
foreach ($service in $services) {
    $envFile = "./$service/.env"
    $envExampleFile = "./$service/.env.example"
    
    if (-not (Test-Path $envFile)) {
        if (Test-Path $envExampleFile) {
            Write-Host "Creating $envFile from example file..." -ForegroundColor Yellow
            Copy-Item $envExampleFile $envFile
            Write-Host "Created $envFile" -ForegroundColor Green
        } else {
            Write-Host "Warning: $envExampleFile not found, cannot create $envFile" -ForegroundColor Yellow
        }
    } else {
        Write-Host "$envFile already exists." -ForegroundColor Green
    }
}

# Ask user which method they want to use
Write-Host ""
Write-Host "How would you like to run the application?" -ForegroundColor Cyan
Write-Host "1. Using Docker (recommended)" -ForegroundColor White
Write-Host "2. Local development (requires PostgreSQL and Redis)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1 or 2)"

if ($choice -eq "1") {
    # Docker approach
    if (-not $dockerRunning) {
        Write-Host "Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "Starting the application using Docker..." -ForegroundColor Yellow
    Write-Host "(This may take a few minutes for the first run)" -ForegroundColor Yellow
    Write-Host ""
    
    docker-compose -f docker-compose.modified.yml up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Services started successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "You can access the application at:" -ForegroundColor Cyan
        Write-Host "- API Gateway: http://localhost:8000" -ForegroundColor White
        Write-Host "- API Documentation: http://localhost:8000/docs" -ForegroundColor White
        Write-Host ""
        Write-Host "To view logs:" -ForegroundColor Cyan
        Write-Host "docker-compose -f docker-compose.modified.yml logs -f" -ForegroundColor White
        Write-Host ""
        Write-Host "To stop the application:" -ForegroundColor Cyan
        Write-Host "docker-compose -f docker-compose.modified.yml down" -ForegroundColor White
    } else {
        Write-Host "Failed to start services." -ForegroundColor Red
        Write-Host "Please check the error messages above." -ForegroundColor Red
        Write-Host ""
        Write-Host "For more troubleshooting help, see DOCKER_TROUBLESHOOTING.md" -ForegroundColor Yellow
    }
} elseif ($choice -eq "2") {
    # Local development approach
    Write-Host ""
    Write-Host "Starting the application using local development..." -ForegroundColor Yellow
    Write-Host ""
    
    # Check if virtual environment exists
    if (-not (Test-Path ".\venv")) {
        Write-Host "Virtual environment not found." -ForegroundColor Yellow
        Write-Host "Creating a new virtual environment..." -ForegroundColor Yellow
        
        python -m venv venv
        if (-not $?) {
            Write-Host "Failed to create virtual environment. Make sure Python is installed." -ForegroundColor Red
            exit 1
        }
        
        Write-Host "Virtual environment created successfully." -ForegroundColor Green
    }
    
    # Activate virtual environment
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
    
    # Install dependencies
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r gateway/requirements.txt
    pip install -r auth-service/requirements.txt
    pip install -r patient-service/requirements.txt
    
    Write-Host ""
    Write-Host "Dependencies installed." -ForegroundColor Green
    Write-Host ""
    Write-Host "To run the application, you need to open three separate terminal windows:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Terminal 1 - Auth Service:" -ForegroundColor White
    Write-Host "cd c:/Users/Hard-Worker/Documents/GitHub/teleHealth/auth-service" -ForegroundColor White
    Write-Host "uvicorn src.main:app --reload --port 8001" -ForegroundColor White
    Write-Host ""
    Write-Host "Terminal 2 - Patient Service:" -ForegroundColor White
    Write-Host "cd c:/Users/Hard-Worker/Documents/GitHub/teleHealth/patient-service" -ForegroundColor White
    Write-Host "uvicorn src.main:app --reload --port 8002" -ForegroundColor White
    Write-Host ""
    Write-Host "Terminal 3 - API Gateway:" -ForegroundColor White
    Write-Host "cd c:/Users/Hard-Worker/Documents/GitHub/teleHealth/gateway" -ForegroundColor White
    Write-Host "uvicorn src.main:app --reload --port 8000" -ForegroundColor White
    Write-Host ""
    Write-Host "After starting all services, you can access the application at:" -ForegroundColor Cyan
    Write-Host "- API Gateway: http://localhost:8000" -ForegroundColor White
    Write-Host "- API Documentation: http://localhost:8000/docs" -ForegroundColor White
} else {
    Write-Host "Invalid choice. Please run the script again and enter 1 or 2." -ForegroundColor Red
}

Write-Host ""
Write-Host "For more information, see the HOW_TO_RUN.md file." -ForegroundColor Cyan
