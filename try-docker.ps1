# PowerShell script to help with Docker troubleshooting

Write-Host "TeleHealth Docker Troubleshooting Helper" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    $dockerStatus = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker does not appear to be running." -ForegroundColor Red
        Write-Host "Please start Docker Desktop and try again." -ForegroundColor Red
        exit 1
    }
    Write-Host "Docker is running." -ForegroundColor Green
} catch {
    Write-Host "Error checking Docker status: $_" -ForegroundColor Red
    Write-Host "Please make sure Docker Desktop is installed and running." -ForegroundColor Red
    exit 1
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

# Try to run the modified docker-compose file
Write-Host ""
Write-Host "Attempting to start services with modified docker-compose file..." -ForegroundColor Yellow
Write-Host "(This may take a few minutes for the first run)" -ForegroundColor Yellow
Write-Host ""

try {
    docker-compose -f docker-compose.modified.yml up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Services started successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "You can access the services at:" -ForegroundColor Cyan
        Write-Host "- API Gateway: http://localhost:8000" -ForegroundColor White
        Write-Host "- API Documentation: http://localhost:8000/docs" -ForegroundColor White
        Write-Host ""
        Write-Host "To view logs:" -ForegroundColor Cyan
        Write-Host "docker-compose -f docker-compose.modified.yml logs -f" -ForegroundColor White
        Write-Host ""
        Write-Host "To stop the services:" -ForegroundColor Cyan
        Write-Host "docker-compose -f docker-compose.modified.yml down" -ForegroundColor White
    } else {
        Write-Host "Failed to start services." -ForegroundColor Red
        Write-Host "Please check the error messages above." -ForegroundColor Red
        Write-Host ""
        Write-Host "For more troubleshooting help, see DOCKER_TROUBLESHOOTING.md" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error running docker-compose: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "For more troubleshooting help, see DOCKER_TROUBLESHOOTING.md" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "If Docker continues to cause issues, you can use the local development approach:" -ForegroundColor Cyan
Write-Host "1. Run .\reload-vscode.ps1 to set up your environment" -ForegroundColor White
Write-Host "2. Follow the instructions in DEVELOPMENT.md for local setup" -ForegroundColor White
