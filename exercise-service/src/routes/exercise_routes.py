from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from ..database import get_db
from ..models.exercise import DifficultyLevel
from ..schemas.exercise import (
    Exercise, 
    ExerciseCreate, 
    ExerciseUpdate, 
    ExerciseList
)
from ..services.exercise_service import ExerciseService
# Import auth utility if needed for protected routes
# from ..utils.auth import get_current_user 

# Configure logging
logger = logging.getLogger("exercise_service.routes.exercise")

# Create router
router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)] # Uncomment to protect all routes
)

@router.post("/", response_model=Exercise, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise: ExerciseCreate,
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection
):
    """Create a new exercise in the library."""
    service = ExerciseService(db)
    # Pass current_user.id if tracking creator
    # exercise.created_by_practitioner_id = current_user.get("id") 
    created_exercise = await service.create_exercise(exercise)
    return created_exercise

@router.get("/", response_model=ExerciseList)
async def get_exercises(
    search: Optional[str] = None,
    difficulty: Optional[DifficultyLevel] = None,
    body_part: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection
):
    """Retrieve exercises with optional filtering and pagination."""
    service = ExerciseService(db)
    exercises, total = await service.get_exercises(
        search=search,
        difficulty=difficulty,
        body_part=body_part,
        page=page,
        page_size=page_size
    )
    return {
        "items": exercises,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/{exercise_id}", response_model=Exercise)
async def get_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection
):
    """Retrieve a specific exercise by ID."""
    service = ExerciseService(db)
    exercise = await service.get_exercise(exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with ID {exercise_id} not found"
        )
    return exercise

@router.put("/{exercise_id}", response_model=Exercise)
async def update_exercise(
    exercise_id: int,
    update_data: ExerciseUpdate,
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection/authorization
):
    """Update an existing exercise."""
    service = ExerciseService(db)
    # Add authorization check: e.g., only creator or admin can update?
    updated_exercise = await service.update_exercise(exercise_id, update_data)
    return updated_exercise

@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection/authorization
):
    """Delete an exercise."""
    service = ExerciseService(db)
    # Add authorization check
    await service.delete_exercise(exercise_id)
    # No return content needed for 204
