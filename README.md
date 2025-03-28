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

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js v18 or higher (for local development)
- Python 3.11 or higher (for local development)

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
# Edit the .env file with your configuration
```

3. Start the application using Docker Compose
```bash
docker-compose up -d
```

4. Access the application
- API Gateway: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Setup

For local development without Docker:

1. Set up the API Gateway
```bash
cd gateway
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

2. Set up other services as they are implemented
```bash
# For each service directory
cd service-name
pip install -r requirements.txt
uvicorn src.main:app --reload --port PORT_NUMBER
```

## Project Structure

```
TeleHealth/
├── gateway/                       # API Gateway
├── appointment-service/           # Appointment management
├── patient-service/               # Patient records and management
├── exercise-service/              # Exercise prescription and library
├── progress-service/              # Progress tracking and analysis
├── communication-service/         # Video consultations and messaging
├── file-service/                  # File storage and management
├── scripts/                       # Utility scripts
└── docker-compose.yml             # Docker deployment configuration
```

## Implementation Status

- ✅ API Gateway
- ✅ Authentication Service
- ✅ Patient Service
- 📝 Appointment Service (Planned)
- 📝 Exercise Service (Planned)
- 📝 Progress Service (Planned)
- 📝 Communication Service (Planned)
- 📝 File Service (Planned)

## Development

We've added comprehensive development guides to help you get started:

- **[DEVELOPMENT.md](./DEVELOPMENT.md)**: Detailed instructions for setting up your development environment
- **[HOW_TO_RUN.md](./HOW_TO_RUN.md)**: Step-by-step guide for running the application
- **[DOCKER_TROUBLESHOOTING.md](./DOCKER_TROUBLESHOOTING.md)**: Solutions for common Docker issues

### Quick Start

The easiest way to run the application is to use our interactive scripts:

#### Option 1: Docker-based Setup

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

#### Option 2: Local Development (Recommended)

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

## Compliance and Security

This platform is designed with healthcare compliance in mind:

- End-to-end encryption for all patient data
- HIPAA-compliant data handling (for US deployments)
- Australian Privacy Principles compliant (for AU deployments)
- Role-based access control
- Comprehensive audit logging

## Roadmap

Future enhancements planned for TeleHealth:

- **Mobile Application**: Native iOS and Android apps for enhanced mobile experience
- **AI-Powered Movement Analysis**: Real-time form correction and movement assessment
- **Wearable Integration**: Connect with fitness trackers and specialized rehabilitation devices
- **Group Therapy**: Support for group rehabilitation sessions
- **Internationalization**: Multi-language support for global deployment

## Contributing

Contributions are welcome! Please check out our contributing guidelines for details on how to get started with development, our coding standards, and the pull request process.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for efficient API development
- [Docker](https://www.docker.com/) for containerization
- [Redis](https://redis.io/) for caching and rate limiting
- [PostgreSQL](https://www.postgresql.org/) for database storage
