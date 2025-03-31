from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base
# Import Exercise if needed for type hinting, but relationship handles DB link
# from .exercise import Exercise 

class ExerciseProgram(Base):
    """
    ExerciseProgram model representing a prescribed set of exercises.
    """
    __tablename__ = "exercise_programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Who created the program and who it's for
    created_by_practitioner_id = Column(Integer, nullable=False, index=True)
    assigned_to_patient_id = Column(Integer, nullable=False, index=True)
    
    # Program duration or goals (optional)
    duration_weeks = Column(Integer, nullable=True)
    goals = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to the association object
    exercise_associations = relationship("ProgramExercise", back_populates="program", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ExerciseProgram(id={self.id}, name='{self.name}', patient_id={self.assigned_to_patient_id})>"


class ProgramExercise(Base):
    """
    Association object linking ExerciseProgram and Exercise.
    Includes details specific to the exercise within the program context.
    """
    __tablename__ = "program_exercises"

    program_id = Column(Integer, ForeignKey("exercise_programs.id"), primary_key=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), primary_key=True)
    
    # Exercise parameters within this program
    order = Column(Integer, nullable=True) # Order of exercise in the program
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    rest_seconds = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True) # Specific notes for this exercise in this program

    # Relationships back to the parent objects
    program = relationship("ExerciseProgram", back_populates="exercise_associations")
    exercise = relationship("Exercise", back_populates="program_associations")

    def __repr__(self):
        return f"<ProgramExercise(program={self.program_id}, exercise={self.exercise_id}, sets={self.sets}, reps={self.reps})>"
