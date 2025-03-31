from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func, and_
from typing import List, Optional, Tuple
from fastapi import HTTPException, status
import logging

from ..database import get_db
from ..models.program import ExerciseProgram, ProgramExercise
from ..models.exercise import Exercise # Needed for validation/linking
from ..schemas.program import ExerciseProgramCreate, ExerciseProgramUpdate

# Configure logging
logger = logging.getLogger("exercise_service.services.program")

class ProgramService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_program(self, program_data: ExerciseProgramCreate) -> ExerciseProgram:
        """Creates a new exercise program and associates exercises."""
        logger.info(f"Creating program '{program_data.name}' for patient {program_data.assigned_to_patient_id}")

        # Basic validation (could add more, e.g., check if patient/practitioner exist via API call)
        if not program_data.exercises:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Program must contain at least one exercise.")

        # Create the main program entry
        db_program = ExerciseProgram(
            name=program_data.name,
            description=program_data.description,
            created_by_practitioner_id=program_data.created_by_practitioner_id,
            assigned_to_patient_id=program_data.assigned_to_patient_id,
            duration_weeks=program_data.duration_weeks,
            goals=program_data.goals
        )
        self.db.add(db_program)

        # Process exercise associations
        exercise_ids = [ex.exercise_id for ex in program_data.exercises]
        
        # Validate that all specified exercises exist (optional but recommended)
        valid_exercises_result = await self.db.execute(
            select(Exercise.id).where(Exercise.id.in_(exercise_ids))
        )
        valid_exercise_ids = {row[0] for row in valid_exercises_result}
        if len(valid_exercise_ids) != len(exercise_ids):
             missing_ids = set(exercise_ids) - valid_exercise_ids
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercises not found: {missing_ids}")

        # Create association objects - must wait for program ID after flush
        try:
            await self.db.flush() # Assigns ID to db_program without committing yet
            
            program_exercises = []
            for ex_assoc_data in program_data.exercises:
                assoc = ProgramExercise(
                    program_id=db_program.id, # Use the flushed ID
                    exercise_id=ex_assoc_data.exercise_id,
                    order=ex_assoc_data.order,
                    sets=ex_assoc_data.sets,
                    reps=ex_assoc_data.reps,
                    duration_seconds=ex_assoc_data.duration_seconds,
                    rest_seconds=ex_assoc_data.rest_seconds,
                    notes=ex_assoc_data.notes
                )
                program_exercises.append(assoc)
            
            self.db.add_all(program_exercises)
            
            await self.db.commit()
            # Refresh the program to load the associations correctly
            # Need to query again with options to load relationships
            refreshed_program = await self.get_program(db_program.id) 
            if not refreshed_program: # Should not happen but safety check
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to reload program after creation")
            logger.info(f"Successfully created program with ID {refreshed_program.id}")
            return refreshed_program
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error creating program: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error creating program")


    async def get_programs(
        self,
        patient_id: Optional[int] = None,
        practitioner_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[ExerciseProgram], int]:
        """Retrieves a list of exercise programs with filtering and pagination."""
        logger.info(f"Getting programs for patient={patient_id}, practitioner={practitioner_id}, page={page}, size={page_size}")
        
        try:
            query = select(ExerciseProgram).options(
                selectinload(ExerciseProgram.exercise_associations).joinedload(ProgramExercise.exercise)
            ) # Eager load associations and nested exercises
            
            filters = []
            if patient_id is not None:
                filters.append(ExerciseProgram.assigned_to_patient_id == patient_id)
            if practitioner_id is not None:
                filters.append(ExerciseProgram.created_by_practitioner_id == practitioner_id)

            if filters:
                query = query.where(and_(*filters))

            count_query = select(func.count()).select_from(query.subquery())
            total_result = await self.db.execute(count_query)
            total = total_result.scalar_one()

            offset = (page - 1) * page_size
            query = query.order_by(ExerciseProgram.created_at.desc()).offset(offset).limit(page_size)

            result = await self.db.execute(query)
            # Use unique() because eager loading can cause duplicate parent rows
            programs = result.scalars().unique().all() 
            
            logger.info(f"Found {len(programs)} programs (total matching: {total})")
            return programs, total
            
        except Exception as e:
            logger.error(f"Database error getting programs: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error retrieving programs")


    async def get_program(self, program_id: int) -> Optional[ExerciseProgram]:
        """Retrieves a specific exercise program by its ID, including exercises."""
        logger.info(f"Getting program with ID {program_id}")
        try:
            result = await self.db.execute(
                select(ExerciseProgram)
                .options(selectinload(ExerciseProgram.exercise_associations).joinedload(ProgramExercise.exercise))
                .where(ExerciseProgram.id == program_id)
            )
            # Use unique() because eager loading can cause duplicate parent rows
            program = result.scalars().unique().first() 
            if not program:
                 logger.warning(f"Program with ID {program_id} not found")
            return program
        except Exception as e:
            logger.error(f"Database error getting program {program_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error retrieving program")

    async def update_program(self, program_id: int, update_data: ExerciseProgramUpdate) -> ExerciseProgram:
        """Updates an existing exercise program's details (excluding exercises)."""
        # Note: Updating exercises within a program is complex (add/remove/update associations).
        # This might be better handled by dedicated endpoints or a more sophisticated update schema.
        # This implementation only updates the ExerciseProgram fields.
        logger.info(f"Updating program with ID {program_id}")
        
        db_program = await self.get_program(program_id) # Fetch with associations
        if not db_program:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Program with ID {program_id} not found")

        update_data_dict = update_data.model_dump(exclude_unset=True)

        for key, value in update_data_dict.items():
            # Ensure we don't try to update relationships directly here
            if hasattr(db_program, key) and key != "exercise_associations": 
                setattr(db_program, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(db_program) 
            # Re-fetch with relationships after refresh if needed, or ensure refresh loads them
            refreshed_program = await self.get_program(db_program.id)
            if not refreshed_program:
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to reload program after update")
            logger.info(f"Successfully updated program with ID {program_id}")
            return refreshed_program
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error updating program {program_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error updating program")

    async def delete_program(self, program_id: int) -> None:
        """Deletes an exercise program and its associations."""
        logger.info(f"Deleting program with ID {program_id}")
        
        db_program = await self.get_program(program_id) # Fetch first to ensure it exists
        if not db_program:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Program with ID {program_id} not found")

        try:
            # Deleting the program should cascade delete associations due to relationship config
            await self.db.delete(db_program)
            await self.db.commit()
            logger.info(f"Successfully deleted program with ID {program_id}")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error deleting program {program_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error deleting program")

    # TODO: Consider adding methods for managing exercises within a program if needed
    # async def add_exercise_to_program(...)
    # async def update_exercise_in_program(...)
    # async def remove_exercise_from_program(...)
