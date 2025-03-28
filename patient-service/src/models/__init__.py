# Patient Service Models Package

from .patient import Patient
from .medical_record import MedicalRecord
from .attachment import Attachment
from .patient_practitioner import PatientPractitioner

# Export all models
__all__ = [
    "Patient",
    "MedicalRecord",
    "Attachment",
    "PatientPractitioner"
]
