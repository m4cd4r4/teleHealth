from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, time
import logging

from ..database import get_db
from ..schemas.schedule import (
    Schedule,
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleList,
    ScheduleSlotCreate,
    ScheduleSlotUpdate,
    ScheduleSlotBulkCreate,
    RecurringScheduleCreate
)
from ..services.schedule_service import ScheduleService
from ..utils.auth import get_current_user

# Configure logging
logger = logging.getLogger("appointment_service.routes.schedule")

# Create router
router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Schedule, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new practitioner schedule.
    
    Parameters:
    - schedule: ScheduleCreate schema with schedule details
    
    Returns:
    - Created schedule data
    """
    logger.info(f"Creating schedule for practitioner {schedule.practitioner_id}")
    
    service = ScheduleService(db)
    try:
        created_schedule = await service.create_schedule(schedule)
        return created_schedule
    except Exception as e:
        logger.error(f"Error creating schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create schedule: {str(e)}"
        )


@router.get("/", response_model=ScheduleList)
async def get_schedules(
    practitioner_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get schedules with optional filtering.
    
    Parameters:
    - practitioner_id: Filter by practitioner ID
    - is_active: Filter by active status
    
    Returns:
    - List of schedules matching criteria
    """
    logger.info(f"Getting schedules with filters: practitioner_id={practitioner_id}, is_active={is_active}")
    
    service = ScheduleService(db)
    schedules, total = await service.get_schedules(
        practitioner_id=practitioner_id,
        is_active=is_active
    )
    
    return {
        "items": schedules,
        "total": total
    }


@router.get("/{schedule_id}", response_model=Schedule)
async def get_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific schedule by ID.
    
    Parameters:
    - schedule_id: ID of the schedule to retrieve
    
    Returns:
    - Schedule data
    """
    logger.info(f"Getting schedule with ID {schedule_id}")
    
    service = ScheduleService(db)
    schedule = await service.get_schedule(schedule_id)
    
    if not schedule:
        logger.error(f"Schedule with ID {schedule_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with ID {schedule_id} not found"
        )
    
    return schedule


@router.get("/practitioner/{practitioner_id}", response_model=Schedule)
async def get_practitioner_schedule(
    practitioner_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get the active schedule for a practitioner.
    
    Parameters:
    - practitioner_id: ID of the practitioner
    
    Returns:
    - Active schedule data
    """
    logger.info(f"Getting active schedule for practitioner {practitioner_id}")
    
    service = ScheduleService(db)
    schedule = await service.get_practitioner_active_schedule(practitioner_id)
    
    if not schedule:
        logger.error(f"No active schedule found for practitioner {practitioner_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active schedule found for practitioner {practitioner_id}"
        )
    
    return schedule


@router.put("/{schedule_id}", response_model=Schedule)
async def update_schedule(
    schedule_id: int,
    update_data: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing schedule.
    
    Parameters:
    - schedule_id: ID of the schedule to update
    - update_data: ScheduleUpdate schema with fields to update
    
    Returns:
    - Updated schedule data
    """
    logger.info(f"Updating schedule with ID {schedule_id}")
    
    service = ScheduleService(db)
    schedule = await service.get_schedule(schedule_id)
    
    if not schedule:
        logger.error(f"Schedule with ID {schedule_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with ID {schedule_id} not found"
        )
    
    try:
        updated_schedule = await service.update_schedule(schedule_id, update_data)
        return updated_schedule
    except Exception as e:
        logger.error(f"Error updating schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not update schedule: {str(e)}"
        )


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a schedule.
    
    Parameters:
    - schedule_id: ID of the schedule to delete
    
    Returns:
    - 204 No Content on success
    """
    logger.info(f"Deleting schedule with ID {schedule_id}")
    
    service = ScheduleService(db)
    schedule = await service.get_schedule(schedule_id)
    
    if not schedule:
        logger.error(f"Schedule with ID {schedule_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with ID {schedule_id} not found"
        )
    
    await service.delete_schedule(schedule_id)


@router.post("/{schedule_id}/slots", response_model=Schedule)
async def add_schedule_slots(
    schedule_id: int,
    slots_data: ScheduleSlotBulkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Add slots to an existing schedule.
    
    Parameters:
    - schedule_id: ID of the schedule to update
    - slots_data: ScheduleSlotBulkCreate schema with slots to add
    
    Returns:
    - Updated schedule data
    """
    logger.info(f"Adding slots to schedule with ID {schedule_id}")
    
    service = ScheduleService(db)
    schedule = await service.get_schedule(schedule_id)
    
    if not schedule:
        logger.error(f"Schedule with ID {schedule_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with ID {schedule_id} not found"
        )
    
    try:
        updated_schedule = await service.add_schedule_slots(schedule_id, slots_data.slots)
        return updated_schedule
    except Exception as e:
        logger.error(f"Error adding slots to schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not add slots to schedule: {str(e)}"
        )


@router.put("/{schedule_id}/slots/{slot_id}", response_model=Schedule)
async def update_schedule_slot(
    schedule_id: int,
    slot_id: int,
    update_data: ScheduleSlotUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update a specific slot in a schedule.
    
    Parameters:
    - schedule_id: ID of the schedule
    - slot_id: ID of the slot to update
    - update_data: ScheduleSlotUpdate schema with fields to update
    
    Returns:
    - Updated schedule data
    """
    logger.info(f"Updating slot {slot_id} in schedule {schedule_id}")
    
    service = ScheduleService(db)
    schedule = await service.get_schedule(schedule_id)
    
    if not schedule:
        logger.error(f"Schedule with ID {schedule_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with ID {schedule_id} not found"
        )
    
    try:
        updated_schedule = await service.update_schedule_slot(schedule_id, slot_id, update_data)
        return updated_schedule
    except Exception as e:
        logger.error(f"Error updating slot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not update slot: {str(e)}"
        )


@router.delete("/{schedule_id}/slots/{slot_id}", response_model=Schedule)
async def delete_schedule_slot(
    schedule_id: int,
    slot_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a specific slot from a schedule.
    
    Parameters:
    - schedule_id: ID of the schedule
    - slot_id: ID of the slot to delete
    
    Returns:
    - Updated schedule data
    """
    logger.info(f"Deleting slot {slot_id} from schedule {schedule_id}")
    
    service = ScheduleService(db)
    schedule = await service.get_schedule(schedule_id)
    
    if not schedule:
        logger.error(f"Schedule with ID {schedule_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with ID {schedule_id} not found"
        )
    
    try:
        updated_schedule = await service.delete_schedule_slot(schedule_id, slot_id)
        return updated_schedule
    except Exception as e:
        logger.error(f"Error deleting slot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not delete slot: {str(e)}"
        )


@router.post("/recurring", response_model=Schedule, status_code=status.HTTP_201_CREATED)
async def create_recurring_schedule(
    practitioner_id: int,
    recurring_data: RecurringScheduleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new schedule with recurring slots based on a pattern.
    
    Parameters:
    - practitioner_id: ID of the practitioner
    - recurring_data: RecurringScheduleCreate schema with pattern details
    
    Returns:
    - Created schedule data
    """
    logger.info(f"Creating recurring schedule for practitioner {practitioner_id} with pattern {recurring_data.pattern}")
    
    service = ScheduleService(db)
    try:
        created_schedule = await service.create_recurring_schedule(
            practitioner_id,
            recurring_data.pattern,
            recurring_data.start_time,
            recurring_data.end_time,
            recurring_data.days
        )
        return created_schedule
    except Exception as e:
        logger.error(f"Error creating recurring schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create recurring schedule: {str(e)}"
        )
