from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

from ..models.notification import NotificationType

class NotificationBase(BaseModel):
    """Base schema for notification data"""
    recipient_id: int
    recipient_type: str  # "patient" or "practitioner"
    notification_type: NotificationType
    subject: Optional[str] = None
    content: str

    @validator('recipient_type')
    def recipient_type_must_be_valid(cls, v):
        """Validate recipient type"""
        valid_types = ['patient', 'practitioner']
        if v not in valid_types:
            raise ValueError(f'recipient_type must be one of {valid_types}')
        return v


class NotificationCreate(NotificationBase):
    """Schema for creating a new notification"""
    appointment_id: int


class NotificationUpdate(BaseModel):
    """Schema for updating an existing notification"""
    subject: Optional[str] = None
    content: Optional[str] = None
    is_sent: Optional[bool] = None
    delivery_status: Optional[str] = None
    
    class Config:
        use_enum_values = True


class NotificationInDB(NotificationBase):
    """Schema for notification in database, including database-specific fields"""
    id: int
    appointment_id: int
    sent_at: Optional[datetime] = None
    is_sent: bool = False
    delivery_status: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class Notification(NotificationInDB):
    """Schema for notification response"""
    class Config:
        orm_mode = True


class NotificationList(BaseModel):
    """Schema for list of notifications"""
    items: List[Notification]
    total: int


class BulkNotificationCreate(BaseModel):
    """Schema for bulk creating notifications"""
    appointment_id: int
    notifications: List[NotificationBase]


class NotificationTemplate(BaseModel):
    """Schema for notification template"""
    template_type: str = Field(..., description="Template type: 'appointment_confirmation', 'appointment_reminder', 'appointment_cancellation', 'appointment_rescheduled'")
    subject: str
    content: str
    notification_type: NotificationType = NotificationType.EMAIL
    
    @validator('template_type')
    def template_type_must_be_valid(cls, v):
        """Validate template type"""
        valid_types = ['appointment_confirmation', 'appointment_reminder', 'appointment_cancellation', 'appointment_rescheduled']
        if v not in valid_types:
            raise ValueError(f'template_type must be one of {valid_types}')
        return v
