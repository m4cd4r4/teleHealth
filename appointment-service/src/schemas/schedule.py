from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, time
from enum import Enum

from ..models.schedule import WeekDay

class ScheduleSlotBase(BaseModel):
    """Base schema for schedule slot data"""
    day_of_week: WeekDay
    start_time: time
    end_time: time
    is_available: bool = True

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        """Validate that end_time is after start_time"""
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class ScheduleSlotCreate(ScheduleSlotBase):
    """Schema for creating a new schedule slot"""
    pass


class ScheduleSlotUpdate(BaseModel):
    """Schema for updating an existing schedule slot"""
    day_of_week: Optional[WeekDay] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_available: Optional[bool] = None
    
    class Config:
        use_enum_values = True


class ScheduleSlotInDB(ScheduleSlotBase):
    """Schema for schedule slot in database, including database-specific fields"""
    id: int
    schedule_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class ScheduleBase(BaseModel):
    """Base schema for schedule data"""
    practitioner_id: int
    name: str = "Default Schedule"
    is_active: bool = True


class ScheduleCreate(ScheduleBase):
    """Schema for creating a new schedule"""
    slots: List[ScheduleSlotCreate]


class ScheduleUpdate(BaseModel):
    """Schema for updating an existing schedule"""
    name: Optional[str] = None
    is_active: Optional[bool] = None
    

class ScheduleInDB(ScheduleBase):
    """Schema for schedule in database, including database-specific fields"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Schedule(ScheduleInDB):
    """Schema for schedule response, including slots"""
    slots: List[ScheduleSlotInDB] = []
    
    class Config:
        orm_mode = True


class ScheduleList(BaseModel):
    """Schema for list of schedules"""
    items: List[Schedule]
    total: int


class ScheduleSlotBulkCreate(BaseModel):
    """Schema for bulk creating schedule slots"""
    slots: List[ScheduleSlotCreate]


class RecurringScheduleCreate(BaseModel):
    """Schema for creating a repeating schedule with preset patterns"""
    pattern: str = Field(..., description="Pattern type: 'weekday', 'weekend', 'daily', 'custom'")
    start_time: time
    end_time: time
    days: Optional[List[WeekDay]] = None  # For custom pattern
    
    @validator('pattern')
    def pattern_must_be_valid(cls, v):
        """Validate pattern type"""
        valid_patterns = ['weekday', 'weekend', 'daily', 'custom']
        if v not in valid_patterns:
            raise ValueError(f'pattern must be one of {valid_patterns}')
        return v
    
    @validator('days', always=True)
    def days_must_be_provided_for_custom(cls, v, values):
        """Validate that days are provided for custom pattern"""
        if values.get('pattern') == 'custom' and (not v or len(v) == 0):
            raise ValueError('days must be provided for custom pattern')
        return v
