#!/usr/bin/env python3
"""
Example usage of the Counseling Session Agent

This script demonstrates how to use the AI agent to process a counseling session
transcript and generate a summary and follow-up email.
"""

import json
from datetime import datetime
from models import SessionTranscript, SessionParticipant, FollowUpEmail
from counseling_agent import CounselingSessionAgent
from email_service import EmailService
import re

def create_sample_transcript():
    """Create a sample counseling session transcript."""
    # Read transcript from file in the transcript folder
    with open("transcript/transcript.txt", "r", encoding="utf-8") as f:
        transcript_text = f.read()
    # Try to extract the student's name from the transcript (first line with 'Counselor:' followed by a reply)
    student_name = "Student"
    for line in transcript_text.splitlines():
        match = re.match(r"([A-Za-z]+):", line.strip())
        if match and match.group(1).lower() not in ["counselor", "dr.", "ms.", "mr.", "mrs."]:
            student_name = match.group(1)
            break
    # Create session participants
    participants = [
        SessionParticipant(
            name="Ms. Patel",  # Default counselor name, can be improved
            role="counselor",
            email="counselor@university.edu"
        ),
        SessionParticipant(
            name=student_name,
            role="student",
            email=f"{student_name.lower()}@university.edu"
        )
    ]
    # Create session transcript
    transcript = SessionTranscript(
        session_id="session_001",
        date=datetime.now(),
        participants=participants,
        transcript=transcript_text,
        duration_minutes=45
    )
    return transcript

def main():
    """Main function to demonstrate the counseling session agent."""
    
    print("🤖 Counseling Session Agent Demo")
    print("=" * 50)
    
    # Initialize the agent
    print("Initializing counseling session agent...")
    agent = CounselingSessionAgent()
    email_service = EmailService()
    
    # Create sample transcript
    print("Creating sample transcript...")
    transcript = create_sample_transcript()
    
    print(f"Session ID: {transcript.session_id}")
    print(f"Student: {next(p.name for p in transcript.participants if p.role == 'student')}")
    print(f"Date: {transcript.date.strftime('%B %d, %Y')}")
    print(f"Duration: {transcript.duration_minutes} minutes")
    print()
    
    # Process the session
    print("Processing session transcript...")
    result = agent.process_session(transcript)
    
    if result.success:
        print("✅ Session processed successfully!")
        print()
        
        # Display session summary
        session_summary = result.data["session_summary"]
        print("📋 SESSION SUMMARY")
        print("-" * 30)
        print(session_summary["summary_text"])
        print()
        
        # Display key takeaways
        print("🎯 KEY TAKEAWAYS")
        print("-" * 30)
        takeaways = result.data["key_takeaways"]
        for category, items in takeaways.items():
            # Skip categories with only the failure message
            if items and not (len(items) == 1 and (items[0] == "Career goal extraction failed" or items[0] == "Action item extraction failed")):
                print(f"{category.replace('_', ' ').title()}:")
                for item in items:
                    print(f"  • {item}")
        print()
        
        # Display follow-up email
        if result.data["follow_up_email"]:
            follow_up_email = result.data["follow_up_email"]
            # If follow_up_email is a dict, convert to FollowUpEmail; if already an object, use directly
            if isinstance(follow_up_email, dict):
                follow_up_email_obj = FollowUpEmail(**follow_up_email)
            else:
                follow_up_email_obj = follow_up_email
            email_service.send_email(follow_up_email_obj)
            # Ask user if they want to save the email template
            save_email = input("Do you want to save the follow-up email template? (y/n): ").strip().lower()
            if save_email in ("y", "yes"):
                template_path = email_service.save_email_template(follow_up_email_obj)
                print(f"✅ Email template saved to: {template_path}")
            else:
                print("Email template was not saved.")
        
    else:
        print(f"❌ Failed to process session: {result.error}")
    
    print("\n" + "=" * 50)
    print("Demo completed!")

if __name__ == "__main__":
    main() 