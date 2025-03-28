from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database import Base

class PatientPractitioner(Base):
    """
    Junction table for the many-to-many relationship between patients and practitioners.
    """
    __tablename__ = "patient_practitioners"

    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True)
    practitioner_id = Column(UUID(as_uuid=True), primary_key=True)
    assigned_date = Column(Date, nullable=False, default=func.current_date())
    access_level = Column(String(50), nullable=False, default="standard")
    is_primary = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<PatientPractitioner patient={self.patient_id} practitioner={self.practitioner_id}>"
