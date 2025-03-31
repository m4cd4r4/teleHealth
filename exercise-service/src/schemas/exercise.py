from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

from ..models.exercise import DifficultyLevel # Assuming enums are defined in models

# Base schema for Exercise properties
class ExerciseBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    instructions: Optional[str] = None
    video_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    difficulty: Optional[DifficultyLevel] = None
    target_body_parts: Optional[str] = Field(None, max_length=255)
    equipment_needed: Optional[str] = Field(None, max_length=255)

# Schema for creating an Exercise (inherits from Base)
class ExerciseCreate(ExerciseBase):
    created_by_practitioner_id: Optional[int] = None # Optional on creation? Or required?

# Schema for updating an Exercise (all fields optional)
class ExerciseUpdate(ExerciseBase):
    name: Optional[str] = Field(None, max_length=255)
    # Make all fields optional for update
    description: Optional[str] = None
    instructions: Optional[str] = None
    video_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    difficulty: Optional[DifficultyLevel] = None
    target_body_parts: Optional[str] = Field(None, max_length=255)
    equipment_needed: Optional[str] = Field(None, max_length=255)

# Schema for reading an Exercise (includes ID and timestamps)
class Exercise(ExerciseBase):
    id: int
    created_by_practitioner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Pydantic V2 uses this instead of orm_mode

# Schema for listing multiple exercises with pagination info
class ExerciseList(BaseModel):
    items: List[Exercise]
    total: int
    page: int
    page_size: int
