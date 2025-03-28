from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Boolean, Text, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database import Base

class Patient(Base):
    """
    Patient model representing a patient in the system.
    """
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    insurance_provider = Column(String(100), nullable=True)
    insurance_number = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"
