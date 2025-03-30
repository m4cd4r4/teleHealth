from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Time, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, time
import enum
from typing import Optional, List

from ..database import Base

class Schedule(Base):
    """
    Practitioner schedule model for defining weekly availability.
    
    This represents a practitioner's regular working schedule, with individual
    time slots defined through the ScheduleSlot relationship.
    """
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    
    # Practitioner ID (from patient service)
    practitioner_id = Column(Integer, nullable=False, index=True, unique=True)
    
    # Schedule details
    name = Column(String(255), nullable=False, default="Default Schedule")
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    slots = relationship("ScheduleSlot", back_populates="schedule", cascade="all, delete-orphan")
    
    def __repr__(self):
        """String representation of the schedule"""
        return f"<Schedule(id={self.id}, practitioner_id={self.practitioner_id}, name={self.name})>"


class WeekDay(int, enum.Enum):
    """Enum for days of the week (0-6)"""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class ScheduleSlot(Base):
    """
    Schedule slot model for defining specific time slots within a schedule.
    
    Each slot represents a specific day of the week and time range when the
    practitioner is available for appointments.
    """
    __tablename__ = "schedule_slots"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to the parent schedule
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    
    # Slot details
    day_of_week = Column(Enum(WeekDay), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    schedule = relationship("Schedule", back_populates="slots")
    
    def __repr__(self):
        """String representation of the schedule slot"""
        return f"<ScheduleSlot(id={self.id}, day={self.day_of_week.name}, start={self.start_time}, end={self.end_time})>"
