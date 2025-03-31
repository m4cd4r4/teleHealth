from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from ..database import get_db
from ..schemas.program import (
    ExerciseProgram, 
    ExerciseProgramCreate, 
    ExerciseProgramUpdate, 
    ExerciseProgramList
)
from ..services.program_service import ProgramService
# Import auth utility if needed
# from ..utils.auth import get_current_user

# Configure logging
logger = logging.getLogger("exercise_service.routes.program")

# Create router
router = APIRouter(
    prefix="/programs",
    tags=["programs"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)] # Uncomment to protect all routes
)

@router.post("/", response_model=ExerciseProgram, status_code=status.HTTP_201_CREATED)
async def create_program(
    program: ExerciseProgramCreate,
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection
):
    """Create a new exercise program."""
    service = ProgramService(db)
    # Add authorization check: e.g., only practitioners can create programs?
    # if current_user.get("role") != "practitioner":
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only practitioners can create programs")
    # program.created_by_practitioner_id = current_user.get("id")
    created_program = await service.create_program(program)
    return created_program

@router.get("/", response_model=ExerciseProgramList)
async def get_programs(
    patient_id: Optional[int] = None,
    practitioner_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection
):
    """Retrieve exercise programs with optional filtering and pagination."""
    # Add authorization: Patients should only see their programs, practitioners theirs or their patients'
    # user_id = current_user.get("id")
    # user_role = current_user.get("role")
    # if user_role == "patient" and (patient_id is None or patient_id != user_id):
    #     patient_id = user_id # Force filter by current patient ID
    # elif user_role == "practitioner" and (practitioner_id is None or practitioner_id != user_id):
    #      # Allow practitioner to see programs they created, or filter by patient
    #      if patient_id is None: # If not filtering by patient, filter by practitioner
    #          practitioner_id = user_id
    
    service = ProgramService(db)
    programs, total = await service.get_programs(
        patient_id=patient_id,
        practitioner_id=practitioner_id,
        page=page,
        page_size=page_size
    )
    return {
        "items": programs,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/{program_id}", response_model=ExerciseProgram)
async def get_program(
    program_id: int,
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection
):
    """Retrieve a specific exercise program by ID."""
    service = ProgramService(db)
    program = await service.get_program(program_id)
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with ID {program_id} not found"
        )
    # Add authorization check: Can current user view this program?
    # user_id = current_user.get("id")
    # user_role = current_user.get("role")
    # if user_role == "patient" and program.assigned_to_patient_id != user_id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this program")
    # elif user_role == "practitioner" and program.created_by_practitioner_id != user_id:
    #     # Practitioners might only see programs they created, or need other logic
    #     pass 
        
    return program

@router.put("/{program_id}", response_model=ExerciseProgram)
async def update_program(
    program_id: int,
    update_data: ExerciseProgramUpdate,
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection/authorization
):
    """Update an existing exercise program's details (exercises not updated here)."""
    service = ProgramService(db)
    # Add authorization check: Only creator can update?
    # program = await service.get_program(program_id) # Fetch first for check
    # if not program or program.created_by_practitioner_id != current_user.get("id"):
    #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this program")
    updated_program = await service.update_program(program_id, update_data)
    return updated_program

@router.delete("/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_program(
    program_id: int,
    db: AsyncSession = Depends(get_db)
    # current_user: dict = Depends(get_current_user) # Add if route needs protection/authorization
):
    """Delete an exercise program."""
    service = ProgramService(db)
    # Add authorization check
    # program = await service.get_program(program_id) # Fetch first for check
    # if not program or program.created_by_practitioner_id != current_user.get("id"):
    #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this program")
    await service.delete_program(program_id)
    # No return content needed for 204

# TODO: Add endpoints for managing exercises within a program if needed
# POST /programs/{program_id}/exercises
# PUT /programs/{program_id}/exercises/{exercise_id}
# DELETE /programs/{program_id}/exercises/{exercise_id}
