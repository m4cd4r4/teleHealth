# TeleHealth API Gateway

The API Gateway is the central entry point for all client requests in the TeleHealth Physiotherapy Platform. It handles authentication, request routing, rate limiting, and logging.

## Features

- **Authentication**: JWT validation and role-based access control
- **Service Discovery**: Routes requests to appropriate microservices
- **Rate Limiting**: Prevents abuse with Redis-based rate limiting
- **Request Logging**: Comprehensive logging for audit purposes
- **CORS Support**: Configurable Cross-Origin Resource Sharing
- **Health Checks**: Monitoring of service health

## Architecture

The API Gateway acts as a reverse proxy, forwarding requests to the appropriate microservices:

- `/api/v1/auth/*` → Authentication Service
- `/api/v1/patients/*` → Patient Service
- `/api/v1/appointments/*` → Appointment Service
- `/api/v1/exercises/*` → Exercise Service
- `/api/v1/progress/*` → Progress Service
- `/api/v1/communications/*` → Communication Service
- `/api/v1/files/*` → File Service

## Prerequisites

- Python 3.11 or higher
- Redis (for rate limiting)
- Docker and Docker Compose (for containerized deployment)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Edit the .env file with your configuration
   ```

## Running Locally

```bash
uvicorn src.main:app --reload --port 8000
```

## Running with Docker

```bash
docker build -t telehealth-gateway .
docker run -p 8000:8000 --env-file .env telehealth-gateway
```

## API Documentation

When the service is running, you can access the Swagger UI documentation at:

```
http://localhost:8000/docs
```

And the ReDoc documentation at:

```
http://localhost:8000/redoc
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| API_GATEWAY_HOST | Host to bind the server to | 0.0.0.0 |
| API_GATEWAY_PORT | Port to bind the server to | 8000 |
| JWT_SECRET_KEY | Secret key for JWT encoding/decoding | (required) |
| JWT_ALGORITHM | Algorithm for JWT | HS256 |
| JWT_ACCESS_TOKEN_EXPIRE_MINUTES | Access token expiry time in minutes | 30 |
| REDIS_HOST | Redis host for rate limiting | redis |
| REDIS_PORT | Redis port | 6379 |
| REDIS_DB | Redis database number | 0 |
| REDIS_PASSWORD | Redis password | (empty) |
| RATE_LIMIT_WINDOW_SECONDS | Rate limit window in seconds | 60 |
| RATE_LIMIT_MAX_REQUESTS | Maximum requests per window | 100 |
| CORS_ORIGINS | List of allowed origins for CORS | ["http://localhost:3000"] |
| AUTH_SERVICE_URL | URL for the Auth Service | http://auth-service:8001 |
| PATIENT_SERVICE_URL | URL for the Patient Service | http://patient-service:8002 |
| APPOINTMENT_SERVICE_URL | URL for the Appointment Service | http://appointment-service:8003 |
| EXERCISE_SERVICE_URL | URL for the Exercise Service | http://exercise-service:8004 |
| PROGRESS_SERVICE_URL | URL for the Progress Service | http://progress-service:8005 |
| COMMUNICATION_SERVICE_URL | URL for the Communication Service | http://communication-service:8006 |
| FILE_SERVICE_URL | URL for the File Service | http://file-service:8007 |
| LOG_LEVEL | Logging level | INFO |

## Development

### Project Structure

```
gateway/
├── src/
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration settings
│   ├── middleware/             # Middleware components
│   ├── routes/                 # Route definitions
│   ├── services/               # Service discovery
│   └── utils/                  # Utility functions
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
└── .env.example                # Example environment variables
```

### Adding a New Service

1. Add the service URL to the `.env` file
2. Add the service type to `src/services/service_registry.py`
3. Create a new route module in `src/routes/`
4. Add the router to `src/routes/__init__.py`
5. Include the router in `src/main.py`

## Testing

```bash
pytest
```

## Security Considerations

- The JWT secret key should be kept secure and rotated periodically
- In production, ensure all communication uses HTTPS
- Regularly update dependencies to patch security vulnerabilities
- Monitor rate limiting and adjust thresholds as needed
