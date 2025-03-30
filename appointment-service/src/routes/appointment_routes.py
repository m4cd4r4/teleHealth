from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from ..database import get_db
from ..models.appointment import AppointmentStatus
from ..schemas.appointment import (
    Appointment, 
    AppointmentCreate, 
    AppointmentUpdate, 
    AppointmentList,
    AppointmentReschedule,
    AppointmentCancel,
    AppointmentComplete,
    AvailabilityResponse
)
from ..services.appointment_service import AppointmentService
from ..utils.auth import get_current_user

# Configure logging
logger = logging.getLogger("appointment_service.routes.appointment")

# Create router
router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new appointment.
    
    Parameters:
    - appointment: AppointmentCreate schema with appointment details
    
    Returns:
    - Created appointment data
    """
    logger.info(f"Creating appointment for patient {appointment.patient_id} with practitioner {appointment.practitioner_id}")
    
    service = AppointmentService(db)
    try:
        created_appointment = await service.create_appointment(appointment)
        return created_appointment
    except Exception as e:
        logger.error(f"Error creating appointment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create appointment: {str(e)}"
        )


@router.get("/", response_model=AppointmentList)
async def get_appointments(
    patient_id: Optional[int] = None,
    practitioner_id: Optional[int] = None,
    status: Optional[AppointmentStatus] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get appointments with optional filtering.
    
    Parameters:
    - patient_id: Filter by patient ID
    - practitioner_id: Filter by practitioner ID
    - status: Filter by appointment status
    - start_date: Filter by appointments after this date
    - end_date: Filter by appointments before this date
    - page: Page number for pagination
    - page_size: Number of items per page
    
    Returns:
    - List of appointments matching criteria
    """
    logger.info(f"Getting appointments with filters: patient_id={patient_id}, practitioner_id={practitioner_id}, status={status}")
    
    service = AppointmentService(db)
    appointments, total = await service.get_appointments(
        patient_id=patient_id,
        practitioner_id=practitioner_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )
    
    return {
        "items": appointments,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{appointment_id}", response_model=Appointment)
async def get_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific appointment by ID.
    
    Parameters:
    - appointment_id: ID of the appointment to retrieve
    
    Returns:
    - Appointment data
    """
    logger.info(f"Getting appointment with ID {appointment_id}")
    
    service = AppointmentService(db)
    appointment = await service.get_appointment(appointment_id)
    
    if not appointment:
        logger.error(f"Appointment with ID {appointment_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    
    return appointment


@router.put("/{appointment_id}", response_model=Appointment)
async def update_appointment(
    appointment_id: int,
    update_data: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing appointment.
    
    Parameters:
    - appointment_id: ID of the appointment to update
    - update_data: AppointmentUpdate schema with fields to update
    
    Returns:
    - Updated appointment data
    """
    logger.info(f"Updating appointment with ID {appointment_id}")
    
    service = AppointmentService(db)
    appointment = await service.get_appointment(appointment_id)
    
    if not appointment:
        logger.error(f"Appointment with ID {appointment_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    
    try:
        updated_appointment = await service.update_appointment(appointment_id, update_data)
        return updated_appointment
    except Exception as e:
        logger.error(f"Error updating appointment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not update appointment: {str(e)}"
        )


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an appointment.
    
    Parameters:
    - appointment_id: ID of the appointment to delete
    
    Returns:
    - 204 No Content on success
    """
    logger.info(f"Deleting appointment with ID {appointment_id}")
    
    service = AppointmentService(db)
    appointment = await service.get_appointment(appointment_id)
    
    if not appointment:
        logger.error(f"Appointment with ID {appointment_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    
    await service.delete_appointment(appointment_id)


@router.post("/{appointment_id}/reschedule", response_model=Appointment)
async def reschedule_appointment(
    appointment_id: int,
    reschedule_data: AppointmentReschedule,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Reschedule an existing appointment.
    
    Parameters:
    - appointment_id: ID of the appointment to reschedule
    - reschedule_data: AppointmentReschedule schema with new time details
    
    Returns:
    - Updated appointment data
    """
    logger.info(f"Rescheduling appointment with ID {appointment_id}")
    
    service = AppointmentService(db)
    appointment = await service.get_appointment(appointment_id)
    
    if not appointment:
        logger.error(f"Appointment with ID {appointment_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    
    try:
        rescheduled_appointment = await service.reschedule_appointment(
            appointment_id, 
            reschedule_data.new_start_time,
            reschedule_data.new_end_time,
            reschedule_data.reason
        )
        return rescheduled_appointment
    except Exception as e:
        logger.error(f"Error rescheduling appointment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not reschedule appointment: {str(e)}"
        )


@router.post("/{appointment_id}/cancel", response_model=Appointment)
async def cancel_appointment(
    appointment_id: int,
    cancel_data: AppointmentCancel,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cancel an existing appointment.
    
    Parameters:
    - appointment_id: ID of the appointment to cancel
    - cancel_data: AppointmentCancel schema with cancellation details
    
    Returns:
    - Updated appointment data
    """
    logger.info(f"Cancelling appointment with ID {appointment_id}")
    
    service = AppointmentService(db)
    appointment = await service.get_appointment(appointment_id)
    
    if not appointment:
        logger.error(f"Appointment with ID {appointment_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    
    try:
        cancelled_appointment = await service.cancel_appointment(
            appointment_id,
            reason=cancel_data.reason,
            notify_patient=cancel_data.notify_patient,
            notify_practitioner=cancel_data.notify_practitioner
        )
        return cancelled_appointment
    except Exception as e:
        logger.error(f"Error cancelling appointment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not cancel appointment: {str(e)}"
        )


@router.post("/{appointment_id}/complete", response_model=Appointment)
async def complete_appointment(
    appointment_id: int,
    complete_data: AppointmentComplete,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Mark an appointment as completed.
    
    Parameters:
    - appointment_id: ID of the appointment to mark as completed
    - complete_data: AppointmentComplete schema with completion details
    
    Returns:
    - Updated appointment data
    """
    logger.info(f"Completing appointment with ID {appointment_id}")
    
    service = AppointmentService(db)
    appointment = await service.get_appointment(appointment_id)
    
    if not appointment:
        logger.error(f"Appointment with ID {appointment_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    
    try:
        completed_appointment = await service.complete_appointment(
            appointment_id,
            notes=complete_data.notes,
            follow_up_required=complete_data.follow_up_required,
            follow_up_in_days=complete_data.follow_up_in_days
        )
        return completed_appointment
    except Exception as e:
        logger.error(f"Error completing appointment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not complete appointment: {str(e)}"
        )


@router.get("/availability/{practitioner_id}", response_model=AvailabilityResponse)
async def get_practitioner_availability(
    practitioner_id: int,
    start_date: datetime = Query(..., description="Start date for availability check"),
    end_date: datetime = Query(..., description="End date for availability check"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get available appointment slots for a practitioner.
    
    Parameters:
    - practitioner_id: ID of the practitioner
    - start_date: Start date for availability window
    - end_date: End date for availability window
    
    Returns:
    - List of available time slots
    """
    logger.info(f"Getting availability for practitioner {practitioner_id} from {start_date} to {end_date}")
    
    # Limit availability window to a maximum of 4 weeks
    max_window = timedelta(days=28)
    if end_date - start_date > max_window:
        end_date = start_date + max_window
    
    service = AppointmentService(db)
    try:
        availability = await service.get_practitioner_availability(
            practitioner_id,
            start_date,
            end_date
        )
        return availability
    except Exception as e:
        logger.error(f"Error getting practitioner availability: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not get availability: {str(e)}"
        )
