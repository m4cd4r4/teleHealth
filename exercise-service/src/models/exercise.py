from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..database import Base

class DifficultyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class BodyPart(str, enum.Enum):
    # Add more specific body parts as needed
    LEGS = "legs"
    ARMS = "arms"
    BACK = "back"
    SHOULDERS = "shoulders"
    CHEST = "chest"
    CORE = "core"
    FULL_BODY = "full_body"
    OTHER = "other"

# Association table for many-to-many relationship between Exercise and BodyPart (if needed)
# Alternatively, could use a simple String/Array field if DB supports it and complex querying isn't needed.
# exercise_body_part_association = Table(
#     'exercise_body_part_association', Base.metadata,
#     Column('exercise_id', Integer, ForeignKey('exercises.id'), primary_key=True),
#     Column('body_part', Enum(BodyPart), primary_key=True) # Or use a separate BodyPart table
# )

class Exercise(Base):
    """
    Exercise model representing an individual exercise in the library.
    """
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    
    # Media links (could point to File Service or external URLs)
    video_url = Column(String(512), nullable=True)
    image_url = Column(String(512), nullable=True)
    
    # Categorization
    difficulty = Column(Enum(DifficultyLevel), nullable=True)
    # Using a simple string for target body parts for now, could normalize later
    target_body_parts = Column(String(255), nullable=True) # e.g., "Legs, Core"
    
    # Equipment needed (simple string for now)
    equipment_needed = Column(String(255), nullable=True) # e.g., "Dumbbells, Resistance Band"

    # Who created this exercise (e.g., system default, specific practitioner)
    created_by_practitioner_id = Column(Integer, nullable=True, index=True) 

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (e.g., linking to programs)
    program_associations = relationship("ProgramExercise", back_populates="exercise")

    def __repr__(self):
        return f"<Exercise(id={self.id}, name='{self.name}')>"
