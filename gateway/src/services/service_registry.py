from enum import Enum
import os

class ServiceType(str, Enum):
    AUTH = "auth"
    PATIENT = "patient"
    APPOINTMENT = "appointment"
    EXERCISE = "exercise"
    PROGRESS = "progress"
    COMMUNICATION = "communication"
    FILE = "file"

class ServiceRegistry:
    def __init__(self):
        # In production, this could be loaded from a service discovery system
        self.services = {
            ServiceType.AUTH: os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001"),
            ServiceType.PATIENT: os.getenv("PATIENT_SERVICE_URL", "http://patient-service:8002"),
            ServiceType.APPOINTMENT: os.getenv("APPOINTMENT_SERVICE_URL", "http://appointment-service:8003"),
            ServiceType.EXERCISE: os.getenv("EXERCISE_SERVICE_URL", "http://exercise-service:8004"),
            ServiceType.PROGRESS: os.getenv("PROGRESS_SERVICE_URL", "http://progress-service:8005"),
            ServiceType.COMMUNICATION: os.getenv("COMMUNICATION_SERVICE_URL", "http://communication-service:8006"),
            ServiceType.FILE: os.getenv("FILE_SERVICE_URL", "http://file-service:8007"),
        }
    
    def get_service_url(self, service_type: ServiceType) -> str:
        return self.services.get(service_type)
    
    def is_service_healthy(self, service_type: ServiceType) -> bool:
        # In a real implementation, this would check the health endpoint
        # For now, we'll assume all services are healthy
        return True

service_registry = ServiceRegistry()
