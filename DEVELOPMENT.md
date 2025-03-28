# TeleHealth Development Guide

This guide provides instructions for setting up your development environment for the TeleHealth project.

## Option 1: Docker Development (Recommended)

Using Docker is the most straightforward approach as it handles all dependencies and environment setup automatically.

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### Steps

1. **Clone the repository** (if you haven't already)
   ```bash
   git clone <repository-url>
   cd teleHealth
   ```

2. **Create environment files**
   ```bash
   # For each service that needs an .env file
   cp gateway/.env.example gateway/.env
   cp auth-service/.env.example auth-service/.env
   cp patient-service/.env.example patient-service/.env
   # ... and so on for other services
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```
   This will:
   - Build all service images
   - Create and start containers
   - Set up the network
   - Initialize the database

4. **Access the services**
   - API Gateway: http://localhost:8000
   - Auth Service: http://localhost:8001
   - Patient Service: http://localhost:8002
   - API Documentation: http://localhost:8000/docs

5. **View logs**
   ```bash
   # View logs for all services
   docker-compose logs -f
   
   # View logs for a specific service
   docker-compose logs -f patient-service
   ```

6. **Stop the services**
   ```bash
   docker-compose down
   ```

## Option 2: Local Development

If you prefer to develop without Docker, you'll need to set up your local environment with the required dependencies.

### Prerequisites

1. **Python 3.11 or higher**
   - [Download Python](https://www.python.org/downloads/)

2. **PostgreSQL**
   - [Download PostgreSQL](https://www.postgresql.org/download/)
   - During installation, note your password and port (default is 5432)
   - Create databases for each service:
     ```sql
     CREATE DATABASE auth_db;
     CREATE DATABASE patient_db;
     CREATE DATABASE appointment_db;
     CREATE DATABASE exercise_db;
     CREATE DATABASE progress_db;
     CREATE DATABASE communication_db;
     CREATE DATABASE file_db;
     ```

3. **Rust and Cargo** (for python-jose)
   - [Install Rust using rustup](https://rustup.rs/)
   - Follow the installation instructions for your platform
   - Verify installation with `rustc --version` and `cargo --version`

4. **Redis** (for rate limiting and caching)
   - [Download Redis](https://redis.io/download)
   - For Windows, use [Redis for Windows](https://github.com/tporadowski/redis/releases)

### Setup Steps

1. **Create a virtual environment**
   ```bash
   # Navigate to the project directory
   cd teleHealth
   
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```

2. **Install dependencies for each service**
   ```bash
   # Install gateway dependencies
   pip install -r gateway/requirements.txt
   
   # Install auth-service dependencies
   pip install -r auth-service/requirements.txt
   
   # Install patient-service dependencies
   pip install -r patient-service/requirements.txt
   
   # ... and so on for other services
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env` for each service
   - Update the database connection strings to point to your local PostgreSQL
   - Update other settings as needed

4. **Run the services**
   ```bash
   # Run each service in a separate terminal window
   
   # Auth Service
   cd auth-service
   uvicorn src.main:app --reload --port 8001
   
   # Patient Service
   cd patient-service
   uvicorn src.main:app --reload --port 8002
   
   # Gateway (run this last)
   cd gateway
   uvicorn src.main:app --reload --port 8000
   ```

## VSCode Configuration

This project includes VSCode settings to improve the development experience:

### Using the Helper Scripts (Recommended)

We've included helper scripts to automate the setup process:

- **Windows**: Run `.\reload-vscode.ps1` in PowerShell
- **macOS/Linux**: Run `./reload-vscode.sh` in Terminal (you may need to make it executable first with `chmod +x reload-vscode.sh`)

These scripts will:
1. Check if VSCode is installed
2. Create a virtual environment if it doesn't exist
3. Activate the virtual environment
4. Open VSCode in the current directory
5. Guide you through the steps to reload VSCode and select the Python interpreter

### Manual Setup

If you prefer to set up manually:

1. **Reload VSCode** to apply the settings:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
   - Type "Developer: Reload Window" and select it

2. **Select the Python interpreter**:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
   - Type "Python: Select Interpreter" and select it
   - Choose the interpreter from your virtual environment

The included settings:
- Disable import error checking to prevent false positives
- Turn off type checking to focus on development
- Enable auto-import completions for better coding experience

## Troubleshooting

### Import Errors in VSCode
- Make sure you've reloaded VSCode after adding the settings
- Verify that you've selected the correct Python interpreter

### PostgreSQL Connection Issues
- Check that PostgreSQL is running: `pg_ctl status`
- Verify your connection string in the `.env` file
- Ensure the databases have been created

### Dependency Installation Problems
- For `psycopg2-binary` issues, ensure PostgreSQL is properly installed
- For `python-jose` issues, verify that Rust and Cargo are installed
- Try installing problematic packages individually with `pip install <package>`

### Docker Issues
- Ensure Docker is running
- Check container logs: `docker-compose logs <service-name>`
- Try rebuilding: `docker-compose build --no-cache`
