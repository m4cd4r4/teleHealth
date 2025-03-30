from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import logging

from ..database import get_db
from ..schemas.notification import (
    Notification,
    NotificationCreate,
    NotificationUpdate,
    NotificationList,
    BulkNotificationCreate,
    NotificationTemplate
)
from ..models.notification import NotificationType
from ..utils.auth import get_current_user, check_admin_permission

# Configure logging
logger = logging.getLogger("appointment_service.routes.notification")

# Create router
router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification: NotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new notification.
    
    Parameters:
    - notification: NotificationCreate schema with notification details
    
    Returns:
    - Created notification data
    """
    logger.info(f"Creating notification for appointment {notification.appointment_id}")
    
    # This is a placeholder - in a real implementation, you would use a notification service
    # that would handle the actual notification creation and sending
    
    return {
        "id": 1,
        "appointment_id": notification.appointment_id,
        "recipient_id": notification.recipient_id,
        "recipient_type": notification.recipient_type,
        "notification_type": notification.notification_type,
        "subject": notification.subject,
        "content": notification.content,
        "sent_at": None,
        "is_sent": False,
        "delivery_status": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@router.get("/", response_model=NotificationList)
async def get_notifications(
    appointment_id: Optional[int] = None,
    recipient_id: Optional[int] = None,
    recipient_type: Optional[str] = None,
    notification_type: Optional[NotificationType] = None,
    is_sent: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get notifications with optional filtering.
    
    Parameters:
    - appointment_id: Filter by appointment ID
    - recipient_id: Filter by recipient ID
    - recipient_type: Filter by recipient type
    - notification_type: Filter by notification type
    - is_sent: Filter by sent status
    - page: Page number for pagination
    - page_size: Number of items per page
    
    Returns:
    - List of notifications matching criteria
    """
    logger.info("Getting notifications with filters")
    
    # Placeholder for demo purposes
    return {
        "items": [],
        "total": 0
    }


@router.get("/{notification_id}", response_model=Notification)
async def get_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific notification by ID.
    
    Parameters:
    - notification_id: ID of the notification to retrieve
    
    Returns:
    - Notification data
    """
    logger.info(f"Getting notification with ID {notification_id}")
    
    # This would fetch the actual notification in a real implementation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Notification with ID {notification_id} not found"
    )


@router.post("/send/{notification_id}", response_model=Notification)
async def send_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Manually send a notification.
    
    Parameters:
    - notification_id: ID of the notification to send
    
    Returns:
    - Updated notification data
    """
    logger.info(f"Sending notification with ID {notification_id}")
    
    # This would send the notification in a real implementation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Notification with ID {notification_id} not found"
    )


@router.post("/bulk", response_model=List[Notification], status_code=status.HTTP_201_CREATED)
async def create_bulk_notifications(
    bulk_data: BulkNotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create multiple notifications for an appointment.
    
    Parameters:
    - bulk_data: BulkNotificationCreate schema with appointment ID and notifications
    
    Returns:
    - List of created notifications
    """
    logger.info(f"Creating bulk notifications for appointment {bulk_data.appointment_id}")
    
    # This would create multiple notifications in a real implementation
    return []


@router.post("/templates", response_model=NotificationTemplate, status_code=status.HTTP_201_CREATED)
async def create_notification_template(
    template: NotificationTemplate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_admin_permission)
):
    """
    Create a new notification template.
    
    Parameters:
    - template: NotificationTemplate schema with template details
    
    Returns:
    - Created template data
    """
    logger.info(f"Creating notification template for type {template.template_type}")
    
    # This would create a notification template in a real implementation
    return template
