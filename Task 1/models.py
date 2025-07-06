from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SessionParticipant(BaseModel):
    """Model for session participants."""
    name: str
    role: str  # "counselor" or "student"
    email: Optional[str] = None

class SessionTranscript(BaseModel):
    """Model for counseling session transcript."""
    session_id: str
    date: datetime
    participants: List[SessionParticipant]
    transcript: str
    duration_minutes: Optional[int] = None

class KeyTakeaway(BaseModel):
    """Model for key takeaways from the session."""
    category: str  # "career_goal", "action_item", "concern", "achievement"
    content: str
    priority: str = "medium"  # "high", "medium", "low"
    assigned_to: Optional[str] = None

class SessionSummary(BaseModel):
    """Model for the generated session summary."""
    session_id: str
    student_name: str
    date: datetime
    key_takeaways: List[KeyTakeaway]
    career_goals: List[str]
    action_items: List[str]
    concerns_addressed: List[str]
    next_steps: List[str]
    summary_text: str
    counselor_notes: Optional[str] = None

class FollowUpEmail(BaseModel):
    """Model for the generated follow-up email."""
    to_email: str
    subject: str
    body: str
    session_summary: SessionSummary
    generated_at: datetime = Field(default_factory=datetime.now)

class AgentResponse(BaseModel):
    """Model for agent response."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None 