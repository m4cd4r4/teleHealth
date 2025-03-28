# PowerShell script to help reload VSCode and select the Python interpreter

Write-Host "TeleHealth Development Environment Setup Helper" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if VSCode is installed
$vscodeCommand = Get-Command code -ErrorAction SilentlyContinue
if (-not $vscodeCommand) {
    Write-Host "Visual Studio Code is not found in your PATH." -ForegroundColor Red
    Write-Host "Please make sure VSCode is installed and 'code' command is available." -ForegroundColor Red
    exit 1
}

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

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. In VSCode, press Ctrl+Shift+P to open the command palette" -ForegroundColor White
Write-Host "2. Type 'Developer: Reload Window' and press Enter" -ForegroundColor White
Write-Host "3. After VSCode reloads, press Ctrl+Shift+P again" -ForegroundColor White
Write-Host "4. Type 'Python: Select Interpreter' and press Enter" -ForegroundColor White
Write-Host "5. Select the interpreter from your virtual environment (it should include 'venv' in the path)" -ForegroundColor White
Write-Host ""
Write-Host "This will apply the VSCode settings and configure the Python environment." -ForegroundColor Cyan

# Open VSCode in the current directory if it's not already open
Write-Host "Opening VSCode in the current directory..." -ForegroundColor Yellow
code .

Write-Host ""
Write-Host "For more information, see the DEVELOPMENT.md file." -ForegroundColor Cyan
