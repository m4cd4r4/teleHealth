from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, and_
from typing import List, Optional, Tuple, Dict
from datetime import datetime, date, time, timedelta
from fastapi import HTTPException, status

from ..models.appointment import Appointment, AppointmentStatus
from ..schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AvailabilityResponse,
)
from ..models.schedule import Schedule, ScheduleSlot, WeekDay
# Import other necessary models/schemas if needed

import logging

# Configure logging
logger = logging.getLogger("appointment_service.services.appointment")

class AppointmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_appointment(self, appointment_data: AppointmentCreate) -> Appointment:
        """Creates a new appointment."""
        logger.info(f"Attempting to create appointment for patient {appointment_data.patient_id} with practitioner {appointment_data.practitioner_id} at {appointment_data.start_time}")

        # --- Validation ---
        # 1. Check if start_time is before end_time
        if appointment_data.start_time >= appointment_data.end_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment start time must be before end time.")

        # 2. Check if the requested slot is available and doesn't conflict
        # Query existing appointments for the practitioner that overlap with the requested time
        conflict_query = select(Appointment).where(
            Appointment.practitioner_id == appointment_data.practitioner_id,
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED, AppointmentStatus.RESCHEDULED]),
            Appointment.start_time < appointment_data.end_time, # Existing starts before new ends
            Appointment.end_time > appointment_data.start_time  # Existing ends after new starts
        )
        conflict_result = await self.db.execute(conflict_query)
        conflicting_appointment = conflict_result.scalars().first()

        if conflicting_appointment:
            logger.warning(f"Booking conflict detected for practitioner {appointment_data.practitioner_id} at {appointment_data.start_time}. Conflicts with appointment ID {conflicting_appointment.id}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"Time slot conflicts with an existing appointment (ID: {conflicting_appointment.id})."
            )
            
        # TODO: Optionally, add a check against the practitioner's schedule using logic similar to get_practitioner_availability
        # This would prevent booking outside working hours, even if there's no direct conflict.

        # --- Creation ---
        # Create Appointment model instance from the schema data
        db_appointment = Appointment(
            patient_id=appointment_data.patient_id,
            practitioner_id=appointment_data.practitioner_id,
            title=appointment_data.title,
            start_time=appointment_data.start_time,
            end_time=appointment_data.end_time,
            status=appointment_data.status if appointment_data.status else AppointmentStatus.SCHEDULED,
            location=appointment_data.location,
            is_virtual=appointment_data.is_virtual,
            meeting_link=appointment_data.meeting_link,
            patient_notes=appointment_data.patient_notes,
            # practitioner_notes are typically added later
        )

        try:
            self.db.add(db_appointment)
            await self.db.commit()
            await self.db.refresh(db_appointment)
            logger.info(f"Successfully created appointment with ID {db_appointment.id}")
            
            # TODO: Trigger notification creation if needed
            
            return db_appointment
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error creating appointment: {str(e)}")
            # Re-raise a more specific exception or handle appropriately
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error during appointment creation")

    async def get_appointments(
        self,
        patient_id: Optional[int] = None,
        practitioner_id: Optional[int] = None,
        status: Optional[AppointmentStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 20
    ) -> (List[Appointment], int):
        """Retrieves a list of appointments with filtering and pagination."""
        logger.info("Getting appointments...")
        # TODO: Implement appointment retrieval logic
        """Retrieves a list of appointments with filtering and pagination."""
        logger.info(f"Getting appointments with filters: patient={patient_id}, practitioner={practitioner_id}, status={status}, start={start_date}, end={end_date}, page={page}, size={page_size}")
        
        try:
            # Base query
            query = select(Appointment)
            
            # Apply filters conditionally
            filters = []
            if patient_id is not None:
                filters.append(Appointment.patient_id == patient_id)
            if practitioner_id is not None:
                filters.append(Appointment.practitioner_id == practitioner_id)
            if status is not None:
                filters.append(Appointment.status == status)
            if start_date is not None:
                filters.append(Appointment.start_time >= start_date)
            if end_date is not None:
                # Assuming end_date is exclusive for the day, adjust if needed
                filters.append(Appointment.start_time < end_date) 
                
            if filters:
                query = query.where(and_(*filters))

            # Get total count for pagination before applying limit/offset
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await self.db.execute(count_query)
            total = total_result.scalar_one()

            # Apply ordering and pagination
            offset = (page - 1) * page_size
            query = query.order_by(Appointment.start_time.desc()).offset(offset).limit(page_size)

            # Execute the main query
            result = await self.db.execute(query)
            appointments = result.scalars().all()
            
            logger.info(f"Found {len(appointments)} appointments (total matching: {total})")
            
            return appointments, total
            
        except Exception as e:
            logger.error(f"Database error getting appointments: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error retrieving appointments")


    async def get_appointment(self, appointment_id: int) -> Optional[Appointment]:
        """Retrieves a specific appointment by its ID."""
        logger.info(f"Getting appointment with ID {appointment_id}...")
        try:
            result = await self.db.execute(
                select(Appointment).where(Appointment.id == appointment_id)
            )
            appointment = result.scalars().first()
            if appointment:
                logger.info(f"Found appointment with ID {appointment_id}")
            else:
                logger.warning(f"Appointment with ID {appointment_id} not found in DB")
            return appointment
        except Exception as e:
            logger.error(f"Database error getting appointment {appointment_id}: {str(e)}")
            # Depending on desired behavior, might re-raise or return None/raise HTTPException
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error retrieving appointment")


    async def update_appointment(self, appointment_id: int, update_data: AppointmentUpdate) -> Appointment:
        """Updates an existing appointment."""
        logger.info(f"Updating appointment with ID {appointment_id}...")
        
        # Fetch the existing appointment
        db_appointment = await self.get_appointment(appointment_id)
        if not db_appointment:
            # get_appointment already logs a warning, but we raise HTTP 404 here
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with ID {appointment_id} not found")

        # Get the update data as a dictionary, excluding unset fields
        update_data_dict = update_data.model_dump(exclude_unset=True)

        # Update the appointment object's attributes
        for key, value in update_data_dict.items():
            if hasattr(db_appointment, key):
                setattr(db_appointment, key, value)
            else:
                logger.warning(f"Attempted to update non-existent attribute '{key}' on appointment {appointment_id}")

        try:
            await self.db.commit()
            await self.db.refresh(db_appointment)
            logger.info(f"Successfully updated appointment with ID {appointment_id}")
            return db_appointment
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error updating appointment {appointment_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error during appointment update")


    async def delete_appointment(self, appointment_id: int) -> None:
        """Deletes an appointment."""
        logger.info(f"Deleting appointment with ID {appointment_id}...")
        
        # Fetch the existing appointment
        db_appointment = await self.get_appointment(appointment_id)
        if not db_appointment:
            # get_appointment already logs a warning, but we raise HTTP 404 here
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with ID {appointment_id} not found")

        try:
            await self.db.delete(db_appointment)
            await self.db.commit()
            logger.info(f"Successfully deleted appointment with ID {appointment_id}")
            # No return value needed for a successful delete (HTTP 204)
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error deleting appointment {appointment_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error during appointment deletion")


    async def reschedule_appointment(
        self, 
        appointment_id: int, 
        new_start_time: datetime, 
        new_end_time: datetime, 
        reason: Optional[str] = None
    ) -> Appointment:
        """Reschedules an existing appointment."""
        logger.info(f"Rescheduling appointment with ID {appointment_id} to {new_start_time} - {new_end_time}")
        
        # Fetch the existing appointment
        db_appointment = await self.get_appointment(appointment_id)
        if not db_appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with ID {appointment_id} not found")

        # --- Validation ---
        # 1. Validate new times
        if new_start_time >= new_end_time:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New start time must be before new end time.")

        # 2. Check for conflicts with other appointments at the new time
        conflict_query = select(Appointment).where(
            Appointment.id != appointment_id, # Exclude the current appointment
            Appointment.practitioner_id == db_appointment.practitioner_id,
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED, AppointmentStatus.RESCHEDULED]),
            Appointment.start_time < new_end_time, # Existing starts before new ends
            Appointment.end_time > new_start_time  # Existing ends after new starts
        )
        conflict_result = await self.db.execute(conflict_query)
        conflicting_appointment = conflict_result.scalars().first()

        if conflicting_appointment:
            logger.warning(f"Reschedule conflict detected for appointment {appointment_id} at {new_start_time}. Conflicts with appointment ID {conflicting_appointment.id}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"Requested reschedule time conflicts with another appointment (ID: {conflicting_appointment.id})."
            )

        # TODO: Optionally, add a check against the practitioner's schedule for the new time slot.

        # --- Update ---
        # Update appointment details
        db_appointment.start_time = new_start_time
        db_appointment.end_time = new_end_time
        db_appointment.status = AppointmentStatus.RESCHEDULED 
        # Optionally add the reason to notes or a dedicated field if it exists
        if reason:
             # Assuming a field like 'reschedule_reason' or appending to notes
             # db_appointment.reschedule_reason = reason 
             logger.info(f"Reschedule reason for appointment {appointment_id}: {reason}")


        try:
            await self.db.commit()
            await self.db.refresh(db_appointment)
            logger.info(f"Successfully rescheduled appointment with ID {appointment_id}")
            
            # TODO: Trigger notification about rescheduling
            
            return db_appointment
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error rescheduling appointment {appointment_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error during appointment reschedule")


    async def cancel_appointment(
        self, 
        appointment_id: int, 
        reason: Optional[str] = None, 
        notify_patient: bool = True, 
        notify_practitioner: bool = True
    ) -> Appointment:
        """Cancels an existing appointment."""
        logger.info(f"Cancelling appointment with ID {appointment_id}")
        
        # Fetch the existing appointment
        db_appointment = await self.get_appointment(appointment_id)
        if not db_appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with ID {appointment_id} not found")

        # Check if already cancelled
        if db_appointment.status == AppointmentStatus.CANCELLED:
             logger.warning(f"Appointment {appointment_id} is already cancelled.")
             # Depending on desired behavior, could return the appointment or raise an error
             return db_appointment # Or raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment already cancelled")

        # Update status and log reason
        db_appointment.status = AppointmentStatus.CANCELLED
        if reason:
            # Assuming a field like 'cancellation_reason' or appending to notes
            # db_appointment.cancellation_reason = reason
            logger.info(f"Cancellation reason for appointment {appointment_id}: {reason}")

        try:
            await self.db.commit()
            await self.db.refresh(db_appointment)
            logger.info(f"Successfully cancelled appointment with ID {appointment_id}")
            
            # TODO: Trigger notifications based on notify_patient and notify_practitioner flags
            if notify_patient:
                logger.info(f"Need to notify patient for cancelled appointment {appointment_id}")
                # Add patient notification logic here
            if notify_practitioner:
                logger.info(f"Need to notify practitioner for cancelled appointment {appointment_id}")
                # Add practitioner notification logic here
                
            return db_appointment
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error cancelling appointment {appointment_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error during appointment cancellation")


    async def complete_appointment(
        self, 
        appointment_id: int, 
        notes: Optional[str] = None, 
        follow_up_required: bool = False, 
        follow_up_in_days: Optional[int] = None
    ) -> Appointment:
        """Marks an appointment as completed."""
        logger.info(f"Completing appointment with ID {appointment_id}")
        
        # Fetch the existing appointment
        db_appointment = await self.get_appointment(appointment_id)
        if not db_appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with ID {appointment_id} not found")

        # Check if already completed or cancelled
        if db_appointment.status in [AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED]:
             logger.warning(f"Appointment {appointment_id} is already {db_appointment.status.value}.")
             # Depending on desired behavior, could return the appointment or raise an error
             return db_appointment # Or raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Appointment already {db_appointment.status.value}")

        # Update status and notes
        db_appointment.status = AppointmentStatus.COMPLETED
        if notes:
            # Assuming practitioner_notes field exists or appending to a general notes field
            db_appointment.practitioner_notes = notes # Or append if needed: db_appointment.practitioner_notes = (db_appointment.practitioner_notes or "") + "\n" + notes
            logger.info(f"Added completion notes for appointment {appointment_id}")

        # Handle follow-up logic (basic example)
        if follow_up_required:
            logger.info(f"Follow-up required for appointment {appointment_id} in {follow_up_in_days} days.")
            # TODO: Implement actual follow-up creation logic
            # This might involve creating a task, a reminder, or another appointment
            # For now, just log it. Could add fields to Appointment model like `follow_up_date`.

        try:
            await self.db.commit()
            await self.db.refresh(db_appointment)
            logger.info(f"Successfully completed appointment with ID {appointment_id}")
            
            # TODO: Trigger notification about completion if needed
            
            return db_appointment
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Database error completing appointment {appointment_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error during appointment completion")


    async def get_practitioner_availability(
        self, 
        practitioner_id: int, 
        start_date: datetime, 
        end_date: datetime
    ) -> AvailabilityResponse:
        """Gets the available time slots for a practitioner within a date range."""
        logger.info(f"Getting availability for practitioner {practitioner_id} from {start_date} to {end_date}")

        # Ensure the date range is reasonable (e.g., max 4 weeks as in routes)
        if end_date - start_date > timedelta(days=28):
             end_date = start_date + timedelta(days=28)
             logger.warning(f"Availability window too large, truncated to 28 days ending {end_date}")

        try:
            # 1. Fetch the practitioner's active schedule and slots
            schedule_result = await self.db.execute(
                select(Schedule)
                .options(selectinload(Schedule.slots)) # Eager load slots
                .where(Schedule.practitioner_id == practitioner_id, Schedule.is_active == True)
            )
            schedule = schedule_result.scalars().first()

            if not schedule or not schedule.slots:
                logger.warning(f"No active schedule or slots found for practitioner {practitioner_id}")
                return AvailabilityResponse(practitioner_id=practitioner_id, available_slots=[])

            # Organize slots by day of week for easier lookup
            schedule_slots_by_day: Dict[int, List[ScheduleSlot]] = {day.value: [] for day in WeekDay}
            for slot in schedule.slots:
                 if slot.is_available:
                    schedule_slots_by_day[slot.day_of_week.value].append(slot)

            # 2. Fetch existing appointments for the practitioner in the range
            appointment_query = select(Appointment).where(
                Appointment.practitioner_id == practitioner_id,
                Appointment.start_time < end_date, # Appointments starting before the end date
                Appointment.end_time > start_date, # Appointments ending after the start date
                Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED, AppointmentStatus.RESCHEDULED]) # Consider only active/upcoming appointments
            )
            appointment_result = await self.db.execute(appointment_query)
            existing_appointments = appointment_result.scalars().all()
            
            # Organize appointments by date for faster lookup
            booked_slots_by_date: Dict[date, List[Tuple[datetime, datetime]]] = {}
            for appt in existing_appointments:
                appt_date = appt.start_time.date()
                if appt_date not in booked_slots_by_date:
                    booked_slots_by_date[appt_date] = []
                booked_slots_by_date[appt_date].append((appt.start_time, appt.end_time))


            # 3. Calculate available slots
            available_slots = []
            current_date = start_date.date()
            end_date_only = end_date.date()
            
            # Assuming a standard appointment duration (e.g., 60 minutes) - this should ideally be configurable
            appointment_duration = timedelta(minutes=60) 

            while current_date < end_date_only:
                day_of_week = current_date.weekday() # Monday is 0, Sunday is 6
                
                # Get schedule slots for this day of the week
                daily_schedule_slots = schedule_slots_by_day.get(day_of_week, [])
                
                # Get booked slots for this specific date
                daily_booked_slots = booked_slots_by_date.get(current_date, [])
                
                for schedule_slot in daily_schedule_slots:
                    # Combine date with schedule time to get datetime objects
                    slot_start_dt = datetime.combine(current_date, schedule_slot.start_time)
                    slot_end_dt = datetime.combine(current_date, schedule_slot.end_time)
                    
                    potential_start = slot_start_dt
                    
                    while potential_start + appointment_duration <= slot_end_dt:
                        potential_end = potential_start + appointment_duration
                        is_booked = False
                        
                        # Check for overlap with booked appointments
                        for booked_start, booked_end in daily_booked_slots:
                            # Check if potential slot overlaps with a booked slot
                            if max(potential_start, booked_start) < min(potential_end, booked_end):
                                is_booked = True
                                break # This potential slot is booked
                                
                        if not is_booked:
                            # Ensure the slot starts at or after the requested start_date (including time)
                            # and ends before the requested end_date (including time)
                            if potential_start >= start_date and potential_end <= end_date:
                                available_slots.append({
                                    "start_time": potential_start,
                                    "end_time": potential_end
                                })
                        
                        # Move to the next potential slot start time
                        # Use a smaller step (e.g., 15 minutes) for finer granularity
                        step_duration = timedelta(minutes=15) 
                        potential_start += step_duration

                current_date += timedelta(days=1)

            logger.info(f"Found {len(available_slots)} available slots for practitioner {practitioner_id}")
            return AvailabilityResponse(practitioner_id=practitioner_id, available_slots=available_slots)

        except Exception as e:
            logger.error(f"Database error getting availability for practitioner {practitioner_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error retrieving availability")
