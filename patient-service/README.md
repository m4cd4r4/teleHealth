# TeleHealth Patient Service

Patient management microservice for the TeleHealth Physiotherapy Platform. This service handles patient profiles, medical records, and patient-practitioner relationships.

## Features

- **Patient Management**: Create, read, update, and delete patient profiles
- **Medical Records**: Manage patient medical history and records
- **Access Control**: Role-based access control for patient data
- **API Documentation**: Interactive API documentation with Swagger UI

## API Endpoints

### Patient Endpoints

- `GET /api/v1/patients`: Get a list of patients with optional filtering
- `GET /api/v1/patients/{patient_id}`: Get a specific patient by ID
- `POST /api/v1/patients`: Create a new patient
- `PUT /api/v1/patients/{patient_id}`: Update a patient
- `DELETE /api/v1/patients/{patient_id}`: Delete a patient

### Medical Record Endpoints

- `GET /api/v1/patients/{patient_id}/medical-records`: Get a patient's medical records
- `POST /api/v1/patients/{patient_id}/medical-records`: Create a new medical record for a patient
- `GET /api/v1/medical-records/{record_id}`: Get a specific medical record
- `PUT /api/v1/medical-records/{record_id}`: Update a medical record
- `DELETE /api/v1/medical-records/{record_id}`: Delete a medical record

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based authentication
- **Documentation**: Swagger UI / OpenAPI

## Setup and Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Docker and Docker Compose (for containerized deployment)

### Local Development Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/telehealth.git
cd telehealth/patient-service
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`
```bash
cp .env.example .env
# Edit the .env file with your configuration
```

5. Run the service
```bash
uvicorn src.main:app --reload --port 8002
```

### Docker Deployment

1. Build the Docker image
```bash
docker build -t telehealth-patient-service .
```

2. Run the container
```bash
docker run -p 8002:8002 --env-file .env telehealth-patient-service
```

Or use Docker Compose from the root directory:
```bash
docker-compose up -d
```

## API Documentation

Once the service is running, you can access the API documentation at:

- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc

## Database Schema

The service uses the following database models:

- **Patient**: Core patient information
- **MedicalRecord**: Patient medical history records
- **Attachment**: File attachments for patients and medical records
- **PatientPractitioner**: Junction table for patient-practitioner relationships

## Authentication and Authorization

This service relies on the Auth Service for authentication. It verifies JWT tokens and enforces role-based access control:

- **Patients** can only access their own data
- **Practitioners** can access data of patients assigned to them
- **Admins** can access all patient data

## Contributing

Please follow the project's coding standards and submit pull requests for any new features or bug fixes.

## License

This project is licensed under the MIT License.
