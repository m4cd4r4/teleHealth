# Patient Service Services Package

from .patient_service import PatientService
from .medical_record_service import MedicalRecordService

# Export all services
__all__ = [
    "PatientService",
    "MedicalRecordService"
]
