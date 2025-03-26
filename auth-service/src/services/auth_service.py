from sqlalchemy.orm import Session
from ..models.user import User, UserRole
from ..utils.password import get_password_hash
from ..utils.jwt_handler import decode_jwt, create_token_with_expiry
from .email_service import EmailService
from datetime import datetime, timedelta
import uuid
import logging

logger = logging.getLogger("auth_service")

class AuthService:
    def __init__(self):
        self.email_service = EmailService()
    
    def get_user_by_email(self, db: Session, email: str) -> User:
        """
        Get a user by email.
        
        Args:
            db: The database session
            email: The user's email
            
        Returns:
            The user or None if not found
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, db: Session, user_id: str) -> User:
        """
        Get a user by ID.
        
        Args:
            db: The database session
            user_id: The user's ID
            
        Returns:
            The user or None if not found
        """
        return db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, db: Session, user_data, user_id: str = None) -> User:
        """
        Create a new user.
        
        Args:
            db: The database session
            user_data: The user data
            user_id: Optional user ID (generated if not provided)
            
        Returns:
            The created user
        """
        if not user_id:
            user_id = str(uuid.uuid4())
        
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            id=user_id,
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"Created user with ID {user_id}")
        
        return db_user
    
    def update_last_login(self, db: Session, user: User):
        """
        Update a user's last login time.
        
        Args:
            db: The database session
            user: The user to update
        """
        user.last_login = datetime.utcnow()
        db.commit()
        
        logger.info(f"Updated last login for user {user.id}")
    
    def verify_user_email(self, db: Session, user: User):
        """
        Mark a user's email as verified.
        
        Args:
            db: The database session
            user: The user to update
        """
        user.email_verified = True
        db.commit()
        
        logger.info(f"Verified email for user {user.id}")
    
    def update_password(self, db: Session, user: User, new_password: str):
        """
        Update a user's password.
        
        Args:
            db: The database session
            user: The user to update
            new_password: The new password
        """
        user.password_hash = get_password_hash(new_password)
        db.commit()
        
        logger.info(f"Updated password for user {user.id}")
    
    def send_verification_email(self, email: str):
        """
        Send an email verification email.
        
        Args:
            email: The recipient's email
        """
        verification_token = create_token_with_expiry(
            {"sub": email, "type": "email_verification"},
            expires_delta=timedelta(hours=24)
        )
        
        verification_link = f"/verify-email/{verification_token}"
        
        self.email_service.send_verification_email(email, verification_link)
        
        logger.info(f"Sent verification email to {email}")
    
    def send_password_reset_email(self, email: str):
        """
        Send a password reset email.
        
        Args:
            email: The recipient's email
        """
        reset_token = create_token_with_expiry(
            {"sub": email, "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        
        reset_link = f"/reset-password/{reset_token}"
        
        self.email_service.send_password_reset_email(email, reset_link)
        
        logger.info(f"Sent password reset email to {email}")
    
    def validate_refresh_token(self, token: str) -> str:
        """
        Validate a refresh token.
        
        Args:
            token: The refresh token
            
        Returns:
            The user ID or None if invalid
        """
        try:
            payload = decode_jwt(token)
            if payload and "sub" in payload:
                return payload["sub"]
        except:
            logger.error("Failed to validate refresh token")
            pass
        return None
    
    def validate_email_verification_token(self, token: str) -> str:
        """
        Validate an email verification token.
        
        Args:
            token: The verification token
            
        Returns:
            The email or None if invalid
        """
        try:
            payload = decode_jwt(token)
            if payload and "sub" in payload and "type" in payload and payload["type"] == "email_verification":
                return payload["sub"]
        except:
            logger.error("Failed to validate email verification token")
            pass
        return None
    
    def validate_password_reset_token(self, token: str) -> str:
        """
        Validate a password reset token.
        
        Args:
            token: The reset token
            
        Returns:
            The email or None if invalid
        """
        try:
            payload = decode_jwt(token)
            if payload and "sub" in payload and "type" in payload and payload["type"] == "password_reset":
                return payload["sub"]
        except:
            logger.error("Failed to validate password reset token")
            pass
        return None
