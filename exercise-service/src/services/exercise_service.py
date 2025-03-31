from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from typing import List, Optional, Tuple
from fastapi import HTTPException, status
import logging

from ..database import get_db
from ..models.exercise import Exercise, DifficultyLevel
from ..schemas.exercise import ExerciseCreate, ExerciseUpdate

# Configure logging
logger = logging.getLogger("exercise_service.services.exercise")

class ExerciseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_exercise(self, exercise_data: ExerciseCreate) -> Exercise:
        """Creates a new exercise in the library."""
        logger.info(f"Creating exercise: {exercise_data.name}")
        
        # Check if exercise with the same name already exists
        existing_exercise = await self.db.execute(
            select(Exercise).where(Exercise.name == exercise_data.name)
        )
        if existing_exercise.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Exercise with name '{exercise_data.name}' already exists."
            )

        db_exercise = Exercise(**exercise_data.model_dump())
        
        try:
            self.db.add(db_exercise)
            await self.db.commit()
            await self.db.refresh(db_exercise)
            logger.info(f"Successfully created exercise with ID {db_exercise.id}")
            return db_exercise
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error creating exercise: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error creating exercise")

    async def get_exercises(
        self,
        search: Optional[str] = None,
        difficulty: Optional[DifficultyLevel] = None,
        body_part: Optional[str] = None, # Assuming simple string search for now
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Exercise], int]:
        """Retrieves a list of exercises with filtering and pagination."""
        logger.info(f"Getting exercises with filters: search={search}, difficulty={difficulty}, body_part={body_part}, page={page}, size={page_size}")
        
        try:
            query = select(Exercise)
            filters = []
            if search:
                # Simple search on name and description
                filters.append(
                    (Exercise.name.ilike(f"%{search}%")) | 
                    (Exercise.description.ilike(f"%{search}%"))
                )
            if difficulty:
                filters.append(Exercise.difficulty == difficulty)
            if body_part:
                 # Simple substring search on the target_body_parts string
                filters.append(Exercise.target_body_parts.ilike(f"%{body_part}%"))

            if filters:
                query = query.where(and_(*filters))

            count_query = select(func.count()).select_from(query.subquery())
            total_result = await self.db.execute(count_query)
            total = total_result.scalar_one()

            offset = (page - 1) * page_size
            query = query.order_by(Exercise.name).offset(offset).limit(page_size)

            result = await self.db.execute(query)
            exercises = result.scalars().all()
            
            logger.info(f"Found {len(exercises)} exercises (total matching: {total})")
            return exercises, total
            
        except Exception as e:
            logger.error(f"Database error getting exercises: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error retrieving exercises")

    async def get_exercise(self, exercise_id: int) -> Optional[Exercise]:
        """Retrieves a specific exercise by its ID."""
        logger.info(f"Getting exercise with ID {exercise_id}")
        try:
            result = await self.db.execute(
                select(Exercise).where(Exercise.id == exercise_id)
            )
            exercise = result.scalars().first()
            if not exercise:
                 logger.warning(f"Exercise with ID {exercise_id} not found")
            return exercise
        except Exception as e:
            logger.error(f"Database error getting exercise {exercise_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error retrieving exercise")

    async def update_exercise(self, exercise_id: int, update_data: ExerciseUpdate) -> Exercise:
        """Updates an existing exercise."""
        logger.info(f"Updating exercise with ID {exercise_id}")
        
        db_exercise = await self.get_exercise(exercise_id)
        if not db_exercise:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with ID {exercise_id} not found")

        update_data_dict = update_data.model_dump(exclude_unset=True)
        
        # Check for name conflict if name is being updated
        if "name" in update_data_dict and update_data_dict["name"] != db_exercise.name:
            existing_exercise = await self.db.execute(
                select(Exercise).where(Exercise.name == update_data_dict["name"], Exercise.id != exercise_id)
            )
            if existing_exercise.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Exercise with name '{update_data_dict['name']}' already exists."
                )

        for key, value in update_data_dict.items():
            setattr(db_exercise, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(db_exercise)
            logger.info(f"Successfully updated exercise with ID {exercise_id}")
            return db_exercise
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error updating exercise {exercise_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error updating exercise")

    async def delete_exercise(self, exercise_id: int) -> None:
        """Deletes an exercise."""
        logger.info(f"Deleting exercise with ID {exercise_id}")
        
        db_exercise = await self.get_exercise(exercise_id)
        if not db_exercise:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with ID {exercise_id} not found")
            
        # TODO: Add check here - should we prevent deletion if exercise is used in programs?
        # if db_exercise.program_associations:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete exercise used in existing programs")

        try:
            await self.db.delete(db_exercise)
            await self.db.commit()
            logger.info(f"Successfully deleted exercise with ID {exercise_id}")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error deleting exercise {exercise_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error deleting exercise")
