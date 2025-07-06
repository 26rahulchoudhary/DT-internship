import json
import logging
from typing import List, Dict, Any
from datetime import datetime

import google.generativeai as genai

from models import (
    SessionTranscript, 
    SessionSummary, 
    FollowUpEmail, 
    KeyTakeaway,
    AgentResponse
)
from config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class CounselingSessionAgent:
    """AI Agent for processing counseling session transcripts and generating summaries and follow-up emails."""
    
    def __init__(self):
        """Initialize the counseling session agent."""
        # Configure Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        # Initialize prompt templates
        self._setup_prompts()
        
    def _setup_prompts(self):
        """Setup prompt templates for different tasks."""
        # Prompt for extracting key takeaways (Colab style)
        self.extract_takeaways_prompt = """
From the following transcript, identify and list:
1. Career Goals mentioned by the participants.
2. Action Items that the participants decided to take.

Format the output clearly with headings for \"Career Goals\" and \"Action Items\".

Transcript:
{transcript}
"""
        
        # Prompt for generating session summary
        self.summary_prompt = """You are a professional career counselor. Create a comprehensive session summary based on the extracted information.

The summary should be:
- Professional yet warm in tone
- Structured and easy to read
- Focused on the student's progress and next steps
- 2-3 paragraphs in length

Include:
- Key discussion points
- Career goals identified
- Action items and deadlines
- Next steps for both student and counselor
- Any resources or tools mentioned

Write in a way that would be helpful for both the student and the counselor's records.

Student: {student_name}
Session Date: {session_date}
Key Information: {key_info}

Please generate a session summary."""
        
        # Prompt for generating follow-up email
        self.email_prompt = """You are a career counselor writing a follow-up email to a student after a counseling session.

Write a friendly, personalized email that:
- Acknowledges the session and thanks the student
- Summarizes key points discussed
- Lists specific action items and deadlines
- Offers encouragement and support
- Provides next steps
- Maintains a warm, professional tone

The email should be:
- Personalized to the student
- Action-oriented
- Encouraging and supportive
- Clear about next steps
- Professional but friendly

Keep it concise (2-3 paragraphs) but comprehensive.

Student Name: {student_name}
Student Email: {student_email}
Session Summary: {session_summary}
Key Action Items: {action_items}

Generate a follow-up email."""
    
    def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API with a prompt and return the response."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            raise
    
    def extract_key_takeaways(self, transcript: str) -> Dict[str, list]:
        """Extract key takeaways from the session transcript using a robust, heading-based approach."""
        try:
            prompt = self.extract_takeaways_prompt.format(transcript=transcript)
            logger.info(f"Sending prompt to Gemini: {prompt[:200]}...")
            response_text = self._call_gemini(prompt)
            # print("[DEBUG] Raw Gemini response for key takeaways:", response_text)
            logger.info(f"Raw Gemini response: {response_text}")
            # Parse the response by headings
            career_goals = []
            action_items = []
            current_section = None
            for line in response_text.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.lower().startswith("career goals"):
                    current_section = "career_goals"
                    continue
                if line.lower().startswith("action items"):
                    current_section = "action_items"
                    continue
                if current_section and (line.startswith('-') or line.startswith('•') or line[0:1].isdigit() or line.startswith('*')):
                    # Remove bullet or number
                    item = line.lstrip('-•*0123456789. ').strip()
                    if item:
                        if current_section == "career_goals":
                            career_goals.append(item)
                        elif current_section == "action_items":
                            action_items.append(item)
            # Fallback if nothing found
            if not career_goals:
                career_goals = ["Career goal extraction failed"]
            if not action_items:
                action_items = ["Action item extraction failed"]
            return {
                "career_goals": career_goals,
                "action_items": action_items,
                "concerns": [],
                "achievements": [],
                "insights": []
            }
        except Exception as e:
            logger.error(f"Error extracting key takeaways: {e}")
            return {
                "career_goals": ["Career goal extraction failed"],
                "action_items": ["Action item extraction failed"],
                "concerns": [],
                "achievements": [],
                "insights": []
            }
    
    def generate_session_summary(self, transcript: SessionTranscript, key_takeaways: Dict[str, List[str]]) -> SessionSummary:
        """Generate a session summary using a simple Gemini prompt."""
        # Find student name
        student_name = next((p.name for p in transcript.participants if p.role == "student"), "Student")
        # Create key takeaways objects
        key_takeaways_objects = []
        for category, items in key_takeaways.items():
            for item in items:
                key_takeaways_objects.append(KeyTakeaway(
                    category=category,
                    content=item,
                    priority="medium"
                ))
        # Use the simple summarization prompt only
        simple_prompt = f"Summarize the following conversation between two people:\n\n{transcript.transcript}"
        summary_text = self._call_gemini(simple_prompt)
        return SessionSummary(
            session_id=transcript.session_id,
            student_name=student_name,
            date=transcript.date,
            key_takeaways=key_takeaways_objects,
            career_goals=key_takeaways.get("career_goals", []),
            action_items=key_takeaways.get("action_items", []),
            concerns_addressed=key_takeaways.get("concerns", []),
            next_steps=key_takeaways.get("action_items", []),  # Use action items as next steps
            summary_text=summary_text
        )
    
    def generate_follow_up_email(self, session_summary: SessionSummary, student_email: str) -> FollowUpEmail:
        """Generate a personalized follow-up email."""
        try:
            # Create subject line
            subject = f"Follow-up: Career Counseling Session - {session_summary.date.strftime('%B %d, %Y')}"
            
            # Generate email body
            action_items_text = "\n".join([f"• {item}" for item in session_summary.action_items])
            
            prompt = self.email_prompt.format(
                student_name=session_summary.student_name,
                student_email=student_email,
                session_summary=session_summary.summary_text,
                action_items=action_items_text
            )
            
            email_body = self._call_gemini(prompt)
            
            return FollowUpEmail(
                to_email=student_email,
                subject=subject,
                body=email_body,
                session_summary=session_summary
            )
            
        except Exception as e:
            logger.error(f"Error generating follow-up email: {e}")
            raise
    
    def process_session(self, transcript: SessionTranscript) -> AgentResponse:
        """Process a counseling session transcript and generate summary and email."""
        try:
            logger.info(f"Processing session {transcript.session_id}")
            
            # Extract key takeaways
            key_takeaways = self.extract_key_takeaways(transcript.transcript)
            logger.info(f"Extracted {sum(len(v) for v in key_takeaways.values())} key takeaways")
            
            # Generate session summary
            session_summary = self.generate_session_summary(transcript, key_takeaways)
            logger.info("Generated session summary")
            
            # Find student email
            student_email = next((p.email for p in transcript.participants if p.role == "student"), None)
            
            # Generate follow-up email if student email is available
            follow_up_email = None
            if student_email:
                follow_up_email = self.generate_follow_up_email(session_summary, student_email)
                logger.info("Generated follow-up email")
            
            return AgentResponse(
                success=True,
                message="Session processed successfully",
                data={
                    "session_summary": session_summary.dict(),
                    "follow_up_email": follow_up_email.dict() if follow_up_email else None,
                    "key_takeaways": key_takeaways
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing session: {e}")
            return AgentResponse(
                success=False,
                message="Failed to process session",
                error=str(e)
            )

def simple_gemini_summary(transcript, api_key, model_name="gemini-2.0-flash"):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    prompt = f"Summarize the following conversation between two people:\n\n{transcript}"
    response = model.generate_content(prompt)
    return response.text 