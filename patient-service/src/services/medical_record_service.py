from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
import uuid
from datetime import date

from ..models.medical_record import MedicalRecord

class MedicalRecordService:
    """
    Service for medical record-related operations.
    """
    
    @staticmethod
    async def get_medical_records(
        db: Session, 
        patient_id: str,
        skip: int = 0, 
        limit: int = 100,
        record_type: Optional[str] = None
    ) -> List[MedicalRecord]:
        """
        Get a list of medical records for a patient.
        
        Args:
            db: Database session
            patient_id: Patient ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            record_type: Optional filter by record type
            
        Returns:
            List of medical records
        """
        query = db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id)
        
        if record_type:
            query = query.filter(MedicalRecord.record_type == record_type)
            
        return query.order_by(MedicalRecord.record_date.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    async def get_medical_record_by_id(
        db: Session, 
        record_id: str
    ) -> Optional[MedicalRecord]:
        """
        Get a medical record by ID.
        
        Args:
            db: Database session
            record_id: Medical record ID
            
        Returns:
            Medical record or None if not found
        """
        return db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    
    @staticmethod
    async def create_medical_record(
        db: Session, 
        record_data: Dict[str, Any]
    ) -> MedicalRecord:
        """
        Create a new medical record.
        
        Args:
            db: Database session
            record_data: Medical record data
            
        Returns:
            Created medical record
            
        Raises:
            HTTPException: If there's an error creating the record
        """
        try:
            record = MedicalRecord(**record_data)
            db.add(record)
            db.commit()
            db.refresh(record)
            return record
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating medical record: {str(e)}"
            )
    
    @staticmethod
    async def update_medical_record(
        db: Session, 
        record_id: str, 
        record_data: Dict[str, Any]
    ) -> Optional[MedicalRecord]:
        """
        Update a medical record.
        
        Args:
            db: Database session
            record_id: Medical record ID
            record_data: Updated medical record data
            
        Returns:
            Updated medical record or None if not found
            
        Raises:
            HTTPException: If there's an error updating the record
        """
        record = await MedicalRecordService.get_medical_record_by_id(db, record_id)
        if not record:
            return None
            
        try:
            for key, value in record_data.items():
                setattr(record, key, value)
                
            db.commit()
            db.refresh(record)
            return record
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error updating medical record: {str(e)}"
            )
    
    @staticmethod
    async def delete_medical_record(db: Session, record_id: str) -> bool:
        """
        Delete a medical record.
        
        Args:
            db: Database session
            record_id: Medical record ID
            
        Returns:
            True if deleted, False if not found
        """
        record = await MedicalRecordService.get_medical_record_by_id(db, record_id)
        if not record:
            return False
            
        db.delete(record)
        db.commit()
        return True
