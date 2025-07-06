from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from counseling_agent import CounselingSessionAgent
from email_service import EmailService
from models import SessionTranscript, AgentResponse
from config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Counseling Session Agent API",
    description="AI Agent for processing counseling session transcripts and generating summaries and follow-up emails",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
counseling_agent = CounselingSessionAgent()
email_service = EmailService()

class ProcessSessionRequest(BaseModel):
    """Request model for processing a session."""
    transcript: SessionTranscript
    send_email: bool = True
    save_email_template: bool = False

class ProcessSessionResponse(BaseModel):
    """Response model for processing a session."""
    success: bool
    message: str
    session_summary: Optional[Dict[str, Any]] = None
    follow_up_email: Optional[Dict[str, Any]] = None
    email_sent: Optional[Dict[str, Any]] = None
    email_template_path: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Counseling Session Agent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "counseling_agent": "initialized",
            "email_service": "initialized"
        }
    }

@app.post("/process-session", response_model=ProcessSessionResponse)
async def process_session(request: ProcessSessionRequest):
    """Process a counseling session transcript and generate summary and email."""
    try:
        logger.info(f"Processing session request for session {request.transcript.session_id}")
        
        # Process the session
        result = counseling_agent.process_session(request.transcript)
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.error)
        
        response_data = {
            "success": True,
            "message": result.message,
            "session_summary": result.data.get("session_summary"),
            "follow_up_email": result.data.get("follow_up_email"),
            "email_sent": None,
            "email_template_path": None
        }
        
        # Send email if requested and available
        if request.send_email and result.data.get("follow_up_email"):
            follow_up_email = result.data["follow_up_email"]
            
            # Send the email
            email_result = email_service.send_email(
                FollowUpEmail(**follow_up_email)
            )
            response_data["email_sent"] = email_result
            
            # Save email template if requested
            if request.save_email_template:
                template_path = email_service.save_email_template(
                    FollowUpEmail(**follow_up_email)
                )
                response_data["email_template_path"] = template_path
        
        return ProcessSessionResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error processing session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-takeaways")
async def extract_takeaways(transcript: str):
    """Extract key takeaways from a transcript."""
    try:
        takeaways = counseling_agent.extract_key_takeaways(transcript)
        return {
            "success": True,
            "takeaways": takeaways
        }
    except Exception as e:
        logger.error(f"Error extracting takeaways: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-email")
async def send_email(email_data: Dict[str, Any]):
    """Send a follow-up email."""
    try:
        follow_up_email = FollowUpEmail(**email_data)
        result = email_service.send_email(follow_up_email)
        
        return {
            "success": result["success"],
            "email_result": result
        }
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        exit(1)
    
    # Run the API server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=Config.DEBUG
    ) 