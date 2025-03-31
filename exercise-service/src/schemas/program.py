from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Import the Exercise schema to nest it in responses
from .exercise import Exercise 

# --- Schemas for ProgramExercise (Association Object) ---

class ProgramExerciseBase(BaseModel):
    """Base schema for properties specific to an exercise within a program."""
    order: Optional[int] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_seconds: Optional[int] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None

class ProgramExerciseCreate(ProgramExerciseBase):
    """Schema for associating an exercise when creating/updating a program."""
    exercise_id: int # Must specify which exercise to add

class ProgramExerciseUpdate(ProgramExerciseBase):
    """Schema for updating an exercise association (all fields optional)."""
    # exercise_id is typically not updatable directly, remove/add instead
    pass 

class ProgramExercise(ProgramExerciseBase):
    """Schema for reading an exercise association, including nested exercise details."""
    exercise_id: int
    exercise: Exercise # Include full Exercise details when reading

    class Config:
        from_attributes = True

# --- Schemas for ExerciseProgram ---

class ExerciseProgramBase(BaseModel):
    """Base schema for ExerciseProgram properties."""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    duration_weeks: Optional[int] = None
    goals: Optional[str] = None

class ExerciseProgramCreate(ExerciseProgramBase):
    """Schema for creating an ExerciseProgram."""
    created_by_practitioner_id: int
    assigned_to_patient_id: int
    exercises: List[ProgramExerciseCreate] # List of exercises to associate

class ExerciseProgramUpdate(ExerciseProgramBase):
    """Schema for updating an ExerciseProgram (all fields optional)."""
    name: Optional[str] = Field(None, max_length=255)
    # Allow updating exercises? This can be complex. Might require separate endpoints.
    # exercises: Optional[List[ProgramExerciseCreate]] = None # Or use specific add/remove endpoints
    pass

class ExerciseProgram(ExerciseProgramBase):
    """Schema for reading an ExerciseProgram, including associated exercises."""
    id: int
    created_by_practitioner_id: int
    assigned_to_patient_id: int
    created_at: datetime
    updated_at: datetime
    exercise_associations: List[ProgramExercise] = [] # Use the detailed association schema

    class Config:
        from_attributes = True

# Schema for listing multiple exercise programs with pagination info
class ExerciseProgramList(BaseModel):
    items: List[ExerciseProgram] # Use the detailed program schema
    total: int
    page: int
    page_size: int
