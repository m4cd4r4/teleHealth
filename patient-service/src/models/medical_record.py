from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from ..database import Base

class MedicalRecord(Base):
    """
    Medical Record model representing a patient's medical history record.
    """
    __tablename__ = "medical_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    record_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    record_date = Column(Date, nullable=False)
    practitioner_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<MedicalRecord {self.record_type} for patient {self.patient_id}>"
