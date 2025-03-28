# How to Run the TeleHealth Application

There are two ways to run the TeleHealth application:

## Option 1: Using Docker (Recommended)

This is the easiest way to run the entire application stack with all services.

### Prerequisites
- Docker Desktop installed and running

### Steps

1. Open a terminal/PowerShell in the teleHealth directory:
   ```
   cd c:/Users/Hard-Worker/Documents/GitHub/teleHealth
   ```

2. Make sure you have the environment files:
   ```
   # Copy example env files if you haven't already
   copy gateway/.env.example gateway/.env
   copy auth-service/.env.example auth-service/.env
   copy patient-service/.env.example patient-service/.env
   ```

3. Run the application using the modified Docker Compose file:
   ```
   docker-compose -f docker-compose.modified.yml up -d
   ```

4. Check if the containers are running:
   ```
   docker ps
   ```
   
   You should see containers for gateway, auth-service, patient-service, redis, and db.

5. If containers are not running or you encounter issues, check the logs:
   ```
   docker-compose -f docker-compose.modified.yml logs
   ```

6. Access the application:
   - API Gateway: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Auth Service: http://localhost:8001
   - Patient Service: http://localhost:8002

7. To stop the application:
   ```
   docker-compose -f docker-compose.modified.yml down
   ```

### Troubleshooting Docker Issues

If you encounter issues with Docker:

1. Make sure Docker Desktop is running
2. Try restarting Docker Desktop
3. Check the Docker logs for specific error messages
4. See the `DOCKER_TROUBLESHOOTING.md` file for more detailed troubleshooting steps
5. Try running the helper script: `.\try-docker.ps1`

## Option 2: Local Development (Recommended)

Since Docker is having issues, we recommend running the services directly on your machine using our new helper scripts.

### Prerequisites
- Python 3.11 or higher
- PostgreSQL installed and running (optional, but required for full functionality)
- Redis installed and running (optional, but required for rate limiting and caching)

### Option A: Using the Interactive Helper Scripts (Easiest)

We've created interactive scripts that guide you through the setup process and let you choose which service to run:

1. For Windows:
   ```
   cd c:/Users/Hard-Worker/Documents/GitHub/teleHealth
   .\run-local.ps1
   ```

2. For macOS/Linux:
   ```
   cd /path/to/teleHealth
   chmod +x run-local.sh
   ./run-local.sh
   ```

These scripts will:
- Create a Python virtual environment if it doesn't exist
- Install all required dependencies
- Check if PostgreSQL and Redis are installed
- Provide instructions for running each service
- Let you choose which service to run in the current terminal

You'll need to run each service (Gateway, Auth Service, and Patient Service) in separate terminals.

### Option B: Manual Setup

If you prefer to set up everything manually:

1. Set up the Python virtual environment:
   ```
   # Windows
   cd c:/Users/Hard-Worker/Documents/GitHub/teleHealth
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   cd /path/to/teleHealth
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies for each service:
   ```
   pip install -r gateway/requirements.txt
   pip install -r auth-service/requirements.txt
   pip install -r patient-service/requirements.txt
   ```

3. Create the necessary databases in PostgreSQL:
   ```sql
   CREATE DATABASE auth_db;
   CREATE DATABASE patient_db;
   ```

4. Run each service in a separate terminal:

   **Terminal 1 - Auth Service:**
   ```
   # Windows
   cd c:/Users/Hard-Worker/Documents/GitHub/teleHealth/auth-service
   .\venv\Scripts\Activate.ps1
   uvicorn src.main:app --reload --port 8001
   
   # macOS/Linux
   cd /path/to/teleHealth/auth-service
   source ../venv/bin/activate
   uvicorn src.main:app --reload --port 8001
   ```

   **Terminal 2 - Patient Service:**
   ```
   # Windows
   cd c:/Users/Hard-Worker/Documents/GitHub/teleHealth/patient-service
   .\venv\Scripts\Activate.ps1
   uvicorn src.main:app --reload --port 8002
   
   # macOS/Linux
   cd /path/to/teleHealth/patient-service
   source ../venv/bin/activate
   uvicorn src.main:app --reload --port 8002
   ```

   **Terminal 3 - API Gateway:**
   ```
   # Windows
   cd c:/Users/Hard-Worker/Documents/GitHub/teleHealth/gateway
   .\venv\Scripts\Activate.ps1
   uvicorn src.main:app --reload --port 8000
   
   # macOS/Linux
   cd /path/to/teleHealth/gateway
   source ../venv/bin/activate
   uvicorn src.main:app --reload --port 8000
   ```

5. Access the application:
   - API Gateway: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Helper Scripts

We've created several helper scripts to make running the application easier:

- `try-docker.ps1` (Windows) or `try-docker.sh` (macOS/Linux): Helps set up and run the Docker environment
- `reload-vscode.ps1` (Windows) or `reload-vscode.sh` (macOS/Linux): Helps set up the local development environment

## Troubleshooting

If you encounter issues:

1. Check the `DOCKER_TROUBLESHOOTING.md` file for Docker-related issues
2. Check the `DEVELOPMENT.md` file for local development setup
3. Make sure all environment variables are properly set in the .env files
4. Verify that PostgreSQL and Redis are running if using local development
