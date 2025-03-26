# TeleHealth Authentication Service

The Authentication Service is responsible for user registration, login, token management, and user authentication in the TeleHealth Physiotherapy Platform.

## Features

- **User Registration**: Create new user accounts with email verification
- **Authentication**: Secure login with JWT tokens
- **Token Management**: Access and refresh tokens with configurable expiry
- **Password Management**: Secure password hashing and reset functionality
- **Role-Based Access Control**: Support for patient, practitioner, and admin roles

## Architecture

The Authentication Service is built with FastAPI and uses PostgreSQL for data storage. It provides a RESTful API for authentication operations and integrates with the API Gateway for centralized authentication.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- SMTP server for email notifications
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
uvicorn src.main:app --reload --port 8001
```

## Running with Docker

```bash
docker build -t telehealth-auth-service .
docker run -p 8001:8001 --env-file .env telehealth-auth-service
```

## API Documentation

When the service is running, you can access the Swagger UI documentation at:

```
http://localhost:8001/docs
```

And the ReDoc documentation at:

```
http://localhost:8001/redoc
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `POST /api/v1/auth/refresh-token` - Refresh an access token
- `POST /api/v1/auth/verify-email/{token}` - Verify email address
- `POST /api/v1/auth/forgot-password` - Request password reset
- `POST /api/v1/auth/reset-password/{token}` - Reset password

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://postgres:postgres@db:5432/auth_db |
| JWT_SECRET_KEY | Secret key for JWT encoding/decoding | (required) |
| JWT_ALGORITHM | Algorithm for JWT | HS256 |
| JWT_ACCESS_TOKEN_EXPIRE_MINUTES | Access token expiry time in minutes | 30 |
| JWT_REFRESH_TOKEN_EXPIRE_DAYS | Refresh token expiry time in days | 7 |
| EMAIL_SENDER | Email address for sending notifications | noreply@telehealth.example.com |
| SMTP_SERVER | SMTP server for sending emails | smtp.example.com |
| SMTP_PORT | SMTP port | 587 |
| SMTP_USERNAME | SMTP username | (required) |
| SMTP_PASSWORD | SMTP password | (required) |
| CORS_ORIGINS | List of allowed origins for CORS | ["http://localhost:3000"] |
| SERVICE_NAME | Service name | auth-service |
| SERVICE_HOST | Host to bind the server to | 0.0.0.0 |
| SERVICE_PORT | Port to bind the server to | 8001 |
| LOG_LEVEL | Logging level | INFO |

## Development

### Project Structure

```
auth-service/
├── src/
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection
│   ├── controllers/            # Request handlers
│   ├── models/                 # Database models
│   ├── routes/                 # API routes
│   ├── services/               # Business logic
│   ├── utils/                  # Utility functions
│   └── templates/              # Email templates
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
└── .env.example                # Example environment variables
```

## Security Considerations

- The JWT secret key should be kept secure and rotated periodically
- In production, ensure all communication uses HTTPS
- Passwords are hashed using bcrypt
- Email verification is required for new accounts
- Password reset tokens expire after 1 hour
- Access tokens expire after 30 minutes by default
- Refresh tokens expire after 7 days by default

## Testing

```bash
pytest
```

## Integration with Other Services

The Authentication Service integrates with:

- **API Gateway**: For centralized authentication
- **Patient Service**: For user profile management
- **Email Service**: For sending verification and password reset emails
