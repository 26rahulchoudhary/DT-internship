import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from datetime import datetime

from models import FollowUpEmail
from config import Config

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending follow-up emails to students."""
    
    def __init__(self):
        """Initialize the email service."""
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.smtp_username = Config.SMTP_USERNAME
        self.smtp_password = Config.SMTP_PASSWORD
        
        # Check if we have SMTP credentials
        self.has_smtp_credentials = bool(self.smtp_username and self.smtp_password)
        
        if not self.has_smtp_credentials:
            logger.warning("SMTP credentials not configured. Email sending will be mocked.")
    
    def send_email(self, email: FollowUpEmail, from_email: str = None) -> Dict[str, Any]:
        """Send a follow-up email to the student."""
        try:
            if not self.has_smtp_credentials:
                return self._mock_send_email(email)
            
            return self._send_via_smtp(email, from_email)
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {
                "success": False,
                "error": str(e),
                "email_id": None,
                "sent_at": datetime.now().isoformat()
            }
    
    def _send_via_smtp(self, email: FollowUpEmail, from_email: str = None) -> Dict[str, Any]:
        """Send email via SMTP server."""
        if not from_email:
            from_email = self.smtp_username
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = email.to_email
        msg['Subject'] = email.subject
        
        # Add body
        msg.attach(MIMEText(email.body, 'plain'))
        
        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {email.to_email}")
        
        return {
            "success": True,
            "email_id": f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "sent_at": datetime.now().isoformat(),
            "to_email": email.to_email,
            "subject": email.subject
        }
    
    def _mock_send_email(self, email: FollowUpEmail) -> Dict[str, Any]:
        """Mock email sending for testing purposes."""
        logger.info(f"MOCK EMAIL SENT:")
        logger.info(f"To: {email.to_email}")
        logger.info(f"Subject: {email.subject}")
        logger.info(f"Body: {email.body[:200]}...")
        
        return {
            "success": True,
            "email_id": f"mock_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "sent_at": datetime.now().isoformat(),
            "to_email": email.to_email,
            "subject": email.subject,
            "mock": True
        }
    
    def save_email_template(self, email: FollowUpEmail, filepath: str = None) -> str:
        """Save email content to a file for review."""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"emails/follow_up_email_{timestamp}.txt"
        
        # Create emails directory if it doesn't exist
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write email content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"To: {email.to_email}\n")
            f.write(f"Subject: {email.subject}\n")
            f.write(f"Generated: {email.generated_at}\n")
            f.write("-" * 50 + "\n")
            f.write(email.body)
        
        logger.info(f"Email template saved to {filepath}")
        return filepath 