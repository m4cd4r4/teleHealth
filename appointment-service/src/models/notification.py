from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from typing import Optional, List

from ..database import Base

class NotificationType(str, enum.Enum):
    """Enum for notification types"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    SYSTEM = "system"


class AppointmentNotification(Base):
    """
    Appointment notification model for storing notification data.
    
    Each notification is associated with an appointment and represents
    a reminder or update sent to a patient or practitioner.
    """
    __tablename__ = "appointment_notifications"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to the appointment
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    
    # Notification details
    recipient_id = Column(Integer, nullable=False, index=True)  # Patient or practitioner ID
    recipient_type = Column(String(20), nullable=False)  # "patient" or "practitioner"
    notification_type = Column(Enum(NotificationType), nullable=False)
    
    # Notification content
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    
    # Notification status
    sent_at = Column(DateTime, nullable=True)
    is_sent = Column(Boolean, default=False)
    delivery_status = Column(String(50), nullable=True)  # "delivered", "failed", etc.
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointment = relationship("Appointment", back_populates="notifications")
    
    def __repr__(self):
        """String representation of the notification"""
        return f"<AppointmentNotification(id={self.id}, type={self.notification_type}, recipient={self.recipient_type}:{self.recipient_id})>"
