#!/usr/bin/env python3
"""
Demo script that shows the Counseling Session Agent structure
without requiring an OpenAI API key.
"""

from datetime import datetime
from models import SessionTranscript, SessionParticipant, SessionSummary, FollowUpEmail, KeyTakeaway

def create_sample_data():
    """Create sample data to demonstrate the system structure."""
    
    # Sample transcript
    transcript = SessionTranscript(
        session_id="demo_session_001",
        date=datetime.now(),
        participants=[
            SessionParticipant(name="Dr. Johnson", role="counselor"),
            SessionParticipant(name="Sarah", role="student", email="sarah@university.edu")
        ],
        transcript="""
        Counselor: Hello Sarah, how are you doing today?
        Sarah: I'm doing well, thank you. I've been thinking about my career goals.
        Counselor: That's great! What specific areas have you been thinking about?
        Sarah: I want to work in software development and learn machine learning.
        Counselor: Excellent! Let's create a plan for you.
        """,
        duration_minutes=45
    )
    
    # Sample key takeaways (what the AI would extract)
    key_takeaways = [
        KeyTakeaway(category="career_goals", content="Work in software development", priority="high"),
        KeyTakeaway(category="career_goals", content="Learn machine learning", priority="high"),
        KeyTakeaway(category="action_items", content="Create a study plan", priority="medium"),
        KeyTakeaway(category="action_items", content="Apply for internships", priority="medium"),
        KeyTakeaway(category="concerns", content="Need to improve technical skills", priority="low"),
    ]
    
    # Sample session summary (what the AI would generate)
    session_summary = SessionSummary(
        session_id="demo_session_001",
        student_name="Sarah",
        date=datetime.now(),
        key_takeaways=key_takeaways,
        career_goals=["Work in software development", "Learn machine learning"],
        action_items=["Create a study plan", "Apply for internships"],
        concerns_addressed=["Need to improve technical skills"],
        next_steps=["Create a study plan", "Apply for internships"],
        summary_text="""
        This session focused on Sarah's career aspirations in software development and machine learning. 
        The student demonstrated clear motivation and has specific goals for her future career path.
        Key action items include creating a structured study plan and applying for relevant internships.
        The counselor provided guidance on next steps and resources for skill development.
        """,
        counselor_notes="Student shows strong motivation and clear direction. Follow up in 2 weeks."
    )
    
    # Sample follow-up email (what the AI would generate)
    follow_up_email = FollowUpEmail(
        to_email="sarah@university.edu",
        subject="Follow-up: Career Counseling Session - December 15, 2024",
        body="""
        Dear Sarah,
        
        Thank you for our productive career counseling session today. I enjoyed discussing your goals in software development and machine learning.
        
        As we discussed, your next steps include:
        • Creating a study plan for your technical skills development
        • Applying for software development and machine learning internships
        • Building a portfolio of projects to showcase your abilities
        
        I'm confident you'll make great progress toward your career goals. Remember to reach out if you need any guidance along the way.
        
        We've scheduled a follow-up meeting in two weeks to review your progress.
        
        Best regards,
        Dr. Johnson
        Career Counselor
        """,
        session_summary=session_summary
    )
    
    return transcript, session_summary, follow_up_email

def main():
    """Main demo function."""
    print("🤖 Counseling Session Agent - Demo (No API Required)")
    print("=" * 60)
    
    # Create sample data
    print("📝 Creating sample counseling session data...")
    transcript, session_summary, follow_up_email = create_sample_data()
    
    print(f"✅ Session ID: {transcript.session_id}")
    print(f"✅ Student: {session_summary.student_name}")
    print(f"✅ Date: {transcript.date.strftime('%B %d, %Y')}")
    print(f"✅ Duration: {transcript.duration_minutes} minutes")
    print()
    
    # Display session summary
    print("📋 SESSION SUMMARY")
    print("-" * 40)
    print(session_summary.summary_text.strip())
    print()
    
    # Display key takeaways
    print("🎯 KEY TAKEAWAYS")
    print("-" * 40)
    for takeaway in session_summary.key_takeaways:
        print(f"• {takeaway.category.replace('_', ' ').title()}: {takeaway.content}")
    print()
    
    # Display career goals
    print("🎯 CAREER GOALS")
    print("-" * 40)
    for goal in session_summary.career_goals:
        print(f"• {goal}")
    print()
    
    # Display action items
    print("📋 ACTION ITEMS")
    print("-" * 40)
    for item in session_summary.action_items:
        print(f"• {item}")
    print()
    
    # Display follow-up email
    print("📧 FOLLOW-UP EMAIL")
    print("-" * 40)
    print(f"To: {follow_up_email.to_email}")
    print(f"Subject: {follow_up_email.subject}")
    print()
    print(follow_up_email.body.strip())
    print()
    
    # Show system capabilities
    print("🔧 SYSTEM CAPABILITIES")
    print("-" * 40)
    print("✅ Process counseling session transcripts")
    print("✅ Extract key takeaways using AI")
    print("✅ Generate professional session summaries")
    print("✅ Create personalized follow-up emails")
    print("✅ Send emails via SMTP or mock service")
    print("✅ REST API for integration")
    print("✅ Comprehensive error handling")
    print("✅ Full test suite")
    print()
    
    print("🚀 NEXT STEPS")
    print("-" * 40)
    print("1. Get an OpenAI API key to enable full AI functionality")
    print("2. Run: python example_usage.py (with API key)")
    print("3. Start API server: python api.py")
    print("4. Test with real counseling transcripts")
    print()
    
    print("=" * 60)
    print("✅ Demo completed! Your AI agent is ready to use.")
    print("💡 Add your OpenAI API key to enable full functionality.")

if __name__ == "__main__":
    main() 