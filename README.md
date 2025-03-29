# TeleHealth Physiotherapy Platform

A comprehensive telehealth solution designed specifically for physiotherapy and rehabilitation services, enabling remote consultations, personalized exercise programs, and continuous patient progress tracking.

## Overview

TeleHealth is a modern, cloud-native platform that connects physiotherapists with patients through secure video consultations and digital health tools. The platform leverages a microservices architecture for scalability, reliability, and flexibility, with separate services handling different aspects of the telehealth experience.

## Key Features

### For Patients
- **Secure Video Consultations**: Connect with your physiotherapist from anywhere
- **Personalized Exercise Programs**: Access custom exercise plans with video demonstrations
- **Progress Tracking**: Monitor your rehabilitation journey with detailed metrics
- **Appointment Management**: Book, reschedule, and manage your appointments
- **Secure Messaging**: Communicate directly with your healthcare provider

### For Practitioners
- **Patient Management**: Maintain comprehensive digital records for your patients
- **Treatment Plan Builder**: Create personalized treatment plans with ease
- **Exercise Prescription**: Assign custom exercise programs with detailed instructions
- **Progress Monitoring**: Track patient adherence and progress in real-time
- **Consultation Tools**: Enhanced video sessions with annotation and recording capabilities

## Technical Architecture

TeleHealth utilizes a modern microservices architecture deployed with Docker and orchestrated with Docker Compose. Each service is independently scalable and maintainable:

- **API Gateway**: Central entry point and authentication service
- **Patient Service**: Patient profiles and medical records management
- **Appointment Service**: Scheduling and appointment management
- **Exercise Service**: Exercise library and prescription management
- **Progress Service**: Progress tracking and analysis
- **Communication Service**: Video consultations and secure messaging
- **File Service**: Secure file storage and management for all media assets

## Technologies Used

### Backend
- **Python** with FastAPI for main microservices
- **Node.js** for the file service
- **PostgreSQL** for persistent data storage
- **Redis** for caching and message queuing
- **JWT** for authentication and authorization

### Frontend
- **React** with TypeScript for type safety
- **React Router** for application routing
- **Zustand** for state management
- **Axios** for API communication
- **WebRTC** for real-time video communication

### DevOps
- **Docker** for containerization
- **Docker Compose** for multi-container orchestration
- **Nginx** for web serving and reverse proxy

## Implementation Status

### Current Services
- ✅ **API Gateway** - Fully implemented with routing, authentication, and rate limiting
- ✅ **Authentication Service** - Complete with user registration, login, JWT token management
- ✅ **Patient Service** - Fully functional with patient profiles and medical records
- 🚧 **Appointment Service** - Basic structure created, implementation in progress
- 🚧 **Exercise Service** - Basic structure created, implementation in progress
- 🚧 **Progress Service** - Basic structure created, implementation in progress
- 🚧 **Communication Service** - Basic structure created, implementation in progress
- 🚧 **File Service** - Basic structure created, implementation in progress

### Current System Capabilities
- User authentication and authorization
- Patient profile management
- Medical record storage and retrieval
- API documentation via Swagger UI
- Rate limiting and security features

## Implemented Services

### API Gateway
The API Gateway serves as the entry point for all client requests, handling:
- Request routing to appropriate microservices
- Authentication and authorization via JWT
- Rate limiting to prevent abuse
- Request/response logging
- API documentation via Swagger UI

**Key Endpoints:**
- `/api/v1/auth/*` - Routes to Authentication Service
- `/api/v1/patients/*` - Routes to Patient Service
- `/docs` - Interactive API documentation

### Authentication Service
The Authentication Service manages user identity and access:
- User registration and account management
- Secure password handling with bcrypt
- JWT token generation and validation
- Role-based access control

**Key Endpoints:**
- `POST /api/v1/auth/register` - Create new user account
- `POST /api/v1/auth/login` - Authenticate and receive JWT
- `GET /api/v1/auth/me` - Get current user profile
- `POST /api/v1/auth/refresh` - Refresh JWT token

### Patient Service
The Patient Service manages patient data and medical records:
- Patient profile creation and management
- Medical history tracking
- Allergy and medication management
- Practitioner assignment

**Key Endpoints:**
- `GET /api/v1/patients` - List patients (for practitioners)
- `GET /api/v1/patients/{id}` - Get patient details
- `POST /api/v1/patients` - Create new patient record
- `PUT /api/v1/patients/{id}` - Update patient information
- `GET /api/v1/patients/{id}/medical-records` - Get patient medical records

## Getting Started

### Prerequisites
- Docker and Docker Compose (for Docker deployment)
- Python 3.11+ (for local development)
- PostgreSQL (for local development)
- Redis (for local development)

### Installation and Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/TeleHealth.git
cd TeleHealth
```

2. Create `.env` files for each service
```bash
# For the API Gateway
cp gateway/.env.example gateway/.env
# For the Auth Service
cp auth-service/.env.example auth-service/.env
# For the Patient Service
cp patient-service/.env.example patient-service/.env
# Edit the .env files with your configuration
```

3. Start the application using Docker Compose
```bash
docker-compose -f docker-compose.modified.yml up -d
```

4. Access the application
- API Gateway: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Auth Service: http://localhost:8001
- Patient Service: http://localhost:8002

## Development

We've added comprehensive development guides to help you get started:

- **[DEVELOPMENT.md](./DEVELOPMENT.md)**: Detailed instructions for setting up your development environment
- **[HOW_TO_RUN.md](./HOW_TO_RUN.md)**: Step-by-step guide for running the application
- **[DOCKER_TROUBLESHOOTING.md](./DOCKER_TROUBLESHOOTING.md)**: Solutions for common Docker issues

### Option 1: Docker-based Setup

- **Windows**: Run `.\run-app.ps1` in PowerShell
- **macOS/Linux**: Run `./run-app.sh` in Terminal (you may need to make it executable first with `chmod +x run-app.sh`)

These scripts will:
1. Check if Docker is running
2. Create necessary environment files
3. Guide you through running the application using either Docker or local development

```bash
# Clone the repository
git clone <repository-url>
cd teleHealth

# Run the interactive script
.\run-app.ps1  # Windows
./run-app.sh   # macOS/Linux

# Or manually:
docker-compose -f docker-compose.modified.yml up -d
```

### Option 2: Local Development

If you're experiencing Docker issues, use our local development scripts:

- **Windows**: Run `.\run-local.ps1` in PowerShell
- **macOS/Linux**: Run `./run-local.sh` in Terminal (you may need to make it executable first with `chmod +x run-local.sh`)

These scripts will:
1. Create a Python virtual environment
2. Install all required dependencies
3. Check if PostgreSQL and Redis are installed
4. Guide you through running each service

```bash
# Clone the repository
git clone <repository-url>
cd teleHealth

# Run the local development script
.\run-local.ps1  # Windows
./run-local.sh   # macOS/Linux
```

For detailed instructions, see [HOW_TO_RUN.md](./HOW_TO_RUN.md).

## Development Roadmap

### Next Phase (Q2 2025)
1. **Appointment Service** - Priority: High
   - Appointment scheduling and management
   - Calendar integration
   - Notifications and reminders

2. **Exercise Service** - Priority: High
   - Exercise library with video demonstrations
   - Custom exercise program creation
   - Exercise tracking and feedback

### Future Phases (Q3-Q4 2025)
3. **Progress Service** - Priority: Medium
   - Patient progress tracking
   - Analytics and reporting
   - Goal setting and achievement tracking

4. **Communication Service** - Priority: Medium
   - Secure video consultations
   - Real-time chat
   - Messaging and notifications

5. **File Service** - Priority: Low
   - Secure file storage
   - Media management
   - Document sharing

## Compliance and Security

This platform is designed with healthcare compliance in mind:

- End-to-end encryption for all patient data
- HIPAA-compliant data handling (for US deployments)
- Australian Privacy Principles compliant (for AU deployments)
- Role-based access control
- Comprehensive audit logging


## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for efficient API development
- [Docker](https://www.docker.com/) for containerization
- [Redis](https://redis.io/) for caching and rate limiting
- [PostgreSQL](https://www.postgresql.org/) for database storage


********************m4cd4r4********************