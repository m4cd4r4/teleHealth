from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import pytz

from ..models.appointment import AppointmentStatus

class AppointmentBase(BaseModel):
    """Base schema for appointment data"""
    patient_id: int
    practitioner_id: int
    title: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_virtual: bool = True
    meeting_link: Optional[str] = None
    patient_notes: Optional[str] = None
    practitioner_notes: Optional[str] = None

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        """Validate that end_time is after start_time"""
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

    @validator('start_time', 'end_time')
    def time_must_be_future(cls, v):
        """Validate that appointment times are in the future"""
        if v < datetime.utcnow():
            raise ValueError('appointment time must be in the future')
        return v


class AppointmentCreate(AppointmentBase):
    """Schema for creating a new appointment"""
    pass


class AppointmentUpdate(BaseModel):
    """Schema for updating an existing appointment"""
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    location: Optional[str] = None
    is_virtual: Optional[bool] = None
    meeting_link: Optional[str] = None
    patient_notes: Optional[str] = None
    practitioner_notes: Optional[str] = None
    
    class Config:
        use_enum_values = True


class AppointmentInDB(AppointmentBase):
    """Schema for appointment in database, including database-specific fields"""
    id: int
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime
    reminders_sent: bool = False
    google_calendar_event_id: Optional[str] = None
    ms_calendar_event_id: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class Appointment(AppointmentInDB):
    """Schema for appointment response, including additional data"""
    notifications: Optional[List[Dict[str, Any]]] = []
    
    class Config:
        orm_mode = True


class AppointmentList(BaseModel):
    """Schema for list of appointments"""
    items: List[Appointment]
    total: int
    page: int
    page_size: int
    

class AppointmentReschedule(BaseModel):
    """Schema for rescheduling an appointment"""
    new_start_time: datetime
    new_end_time: datetime
    reason: Optional[str] = None

    @validator('new_end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        """Validate that end_time is after start_time"""
        if 'new_start_time' in values and v <= values['new_start_time']:
            raise ValueError('new_end_time must be after new_start_time')
        return v

    @validator('new_start_time', 'new_end_time')
    def time_must_be_future(cls, v):
        """Validate that appointment times are in the future"""
        if v < datetime.utcnow():
            raise ValueError('appointment time must be in the future')
        return v


class AppointmentCancel(BaseModel):
    """Schema for cancelling an appointment"""
    reason: Optional[str] = None
    notify_patient: bool = True
    notify_practitioner: bool = True


class AppointmentComplete(BaseModel):
    """Schema for completing an appointment"""
    notes: Optional[str] = None
    follow_up_required: bool = False
    follow_up_in_days: Optional[int] = None


class TimeSlot(BaseModel):
    """Schema for representing an available time slot"""
    start_time: datetime
    end_time: datetime
    practitioner_id: int


class AvailableSlotList(BaseModel):
    """Schema for list of available time slots"""
    date: str
    slots: List[TimeSlot]


class AvailabilityResponse(BaseModel):
    """Schema for availability response"""
    days: List[AvailableSlotList]
