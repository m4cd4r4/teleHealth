# Docker Troubleshooting Guide for TeleHealth

This guide addresses common Docker issues you might encounter when setting up the TeleHealth project.

## Current Issue: Unable to Pull Python Image

You're encountering the following error:
```
unable to get image 'python:3.11-slim': request returned Internal Server Error for API route and version http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.47/images/python:3.11-slim/json, check if the server supports the requested API version
```

### Solution 1: Use Modified Docker Compose File

I've created a modified Docker Compose file that removes the placeholder services that were causing the issue. Try running:

```bash
docker-compose -f docker-compose.modified.yml up -d
```

This modified file includes only the essential services (gateway, auth-service, patient-service, redis, and db) and removes the placeholder services that were using the problematic Python image.

### Solution 2: Restart Docker Desktop

The error suggests there might be an issue with the Docker Desktop service:

1. Close Docker Desktop completely
2. Open Task Manager (Ctrl+Shift+Esc)
3. Check for any Docker processes and end them
4. Restart Docker Desktop
5. Wait for Docker to fully initialize
6. Try running the command again:
   ```bash
   docker-compose up -d
   ```

### Solution 3: Check Docker Network Settings

Sometimes Docker network settings can cause issues:

1. Open Docker Desktop
2. Go to Settings > Resources > Network
3. Make sure "Use WSL 2 based engine" is enabled (if you're using WSL)
4. Click "Apply & Restart"

### Solution 4: Pull Images Manually

Try pulling the problematic image manually to see more detailed error messages:

```bash
docker pull python:3.11-slim
```

If this fails, try an alternative image:

```bash
docker pull python:3.11-alpine
```

Then modify the docker-compose.yml file to use the alternative image.

## Alternative Approach: Local Development

If Docker continues to cause issues, you can use the local development approach as described in the DEVELOPMENT.md file:

1. Run the helper script to set up your environment:
   ```bash
   # For Windows
   .\reload-vscode.ps1
   ```

2. Install PostgreSQL and Redis locally:
   - [PostgreSQL Download](https://www.postgresql.org/download/)
   - [Redis for Windows](https://github.com/tporadowski/redis/releases)

3. Create the necessary databases:
   ```sql
   CREATE DATABASE auth_db;
   CREATE DATABASE patient_db;
   ```

4. Install dependencies for each service:
   ```bash
   pip install -r gateway/requirements.txt
   pip install -r auth-service/requirements.txt
   pip install -r patient-service/requirements.txt
   ```

5. Run each service in a separate terminal:
   ```bash
   # Auth Service
   cd auth-service
   uvicorn src.main:app --reload --port 8001

   # Patient Service
   cd patient-service
   uvicorn src.main:app --reload --port 8002

   # Gateway
   cd gateway
   uvicorn src.main:app --reload --port 8000
   ```

## General Docker Troubleshooting Tips

### Check Docker Status
```bash
docker info
```

### View Docker Logs
```bash
docker logs <container_id>
```

### Reset Docker
If all else fails, you can reset Docker to its factory settings:
1. Open Docker Desktop
2. Go to Settings > Troubleshoot
3. Click "Reset to factory defaults"
4. Restart Docker Desktop

### Update Docker
Make sure you're running the latest version of Docker Desktop.

## Need More Help?

If you continue to experience issues, please:
1. Check the Docker Desktop logs
2. Visit the [Docker troubleshooting guide](https://docs.docker.com/desktop/troubleshoot/overview/)
3. Search for your specific error message on Stack Overflow
