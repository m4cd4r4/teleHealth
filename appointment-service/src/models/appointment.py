from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from typing import Optional, List

from ..database import Base

class AppointmentStatus(str, enum.Enum):
    """Enum for appointment status"""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"


class Appointment(Base):
    """
    Appointment model for storing appointment data.
    
    Relationships:
    - Each appointment is associated with a patient and practitioner (by ID)
    - Appointments are associated with notifications for reminders
    """
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    
    # Patient and practitioner IDs (from patient service)
    patient_id = Column(Integer, nullable=False, index=True)
    practitioner_id = Column(Integer, nullable=False, index=True)
    
    # Appointment details
    title = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED, nullable=False)
    
    # Location and type
    location = Column(String(255), nullable=True)
    is_virtual = Column(Boolean, default=True, nullable=False)
    meeting_link = Column(String(255), nullable=True)
    
    # Notes and other details
    patient_notes = Column(Text, nullable=True)
    practitioner_notes = Column(Text, nullable=True)
    
    # Reminders and notifications
    reminders_sent = Column(Boolean, default=False)
    
    # External calendar references
    google_calendar_event_id = Column(String(255), nullable=True)
    ms_calendar_event_id = Column(String(255), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    notifications = relationship("AppointmentNotification", back_populates="appointment", cascade="all, delete-orphan")
    
    def __repr__(self):
        """String representation of the appointment"""
        return f"<Appointment(id={self.id}, patient_id={self.patient_id}, practitioner_id={self.practitioner_id}, start_time={self.start_time})>"
