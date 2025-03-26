import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from ..config import settings
import os
import logging

logger = logging.getLogger("auth_service")

class EmailService:
    def __init__(self):
        self.sender_email = settings.EMAIL_SENDER
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        
        # Set up Jinja2 for email templates
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
        
        # Create template directory if it doesn't exist
        os.makedirs(template_dir, exist_ok=True)
        
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def send_email(self, to_email: str, subject: str, template_name: str, template_data: dict) -> bool:
        """
        Send an email using a template.
        
        Args:
            to_email: The recipient's email address
            subject: The email subject
            template_name: The name of the template to use
            template_data: The data to pass to the template
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = to_email
        
        try:
            # Render template
            template = self.env.get_template(f"{template_name}.html")
            html = template.render(**template_data)
            
            # Attach HTML content
            part = MIMEText(html, "html")
            message.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
                logger.info(f"Email sent to {to_email}")
                return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_verification_email(self, to_email: str, verification_link: str) -> bool:
        """
        Send an email verification email.
        
        Args:
            to_email: The recipient's email address
            verification_link: The verification link
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        subject = "Verify Your TeleHealth Account"
        template_data = {
            "verification_link": verification_link
        }
        return self.send_email(to_email, subject, "email_verification", template_data)
    
    def send_password_reset_email(self, to_email: str, reset_link: str) -> bool:
        """
        Send a password reset email.
        
        Args:
            to_email: The recipient's email address
            reset_link: The password reset link
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        subject = "Reset Your TeleHealth Password"
        template_data = {
            "reset_link": reset_link
        }
        return self.send_email(to_email, subject, "password_reset", template_data)
