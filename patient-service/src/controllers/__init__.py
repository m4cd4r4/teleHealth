# Patient Service Controllers Package

from .patient_controller import PatientController
from .medical_record_controller import MedicalRecordController

# Export all controllers
__all__ = [
    "PatientController",
    "MedicalRecordController"
]
