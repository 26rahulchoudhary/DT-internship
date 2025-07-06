# #!/usr/bin/env python3
# """
# Test script for the Counseling Session Agent

# This script tests the core functionality of the AI agent without requiring
# an actual Gemini API key (uses mock responses).
# """

# import json
# import unittest
# from unittest.mock import Mock, patch
# from datetime import datetime

# from models import SessionTranscript, SessionParticipant, AgentResponse
# from counseling_agent import CounselingSessionAgent

# class TestCounselingSessionAgent(unittest.TestCase):
#     """Test cases for the CounselingSessionAgent class."""
    
#     def setUp(self):
#         """Set up test fixtures."""
#         # Create a sample transcript for testing
#         self.sample_transcript = SessionTranscript(
#             session_id="test_session_001",
#             date=datetime.now(),
#             participants=[
#                 SessionParticipant(name="Dr. Test", role="counselor"),
#                 SessionParticipant(name="Test Student", role="student", email="test@university.edu")
#             ],
#             transcript="""
#             Counselor: Hello, how are you doing today?
#             Student: I'm doing well, thank you. I've been thinking about my career goals.
#             Counselor: That's great! What specific goals do you have?
#             Student: I want to work in software development and learn machine learning.
#             Counselor: Excellent! Let's create a plan for you.
#             Student: That would be very helpful.
#             """,
#             duration_minutes=30
#         )
        
#         # Mock LLM responses
#         self.mock_takeaways_response = {
#             "career_goals": ["Work in software development", "Learn machine learning"],
#             "action_items": ["Create a study plan", "Apply for internships"],
#             "concerns": ["Need to improve technical skills"],
#             "achievements": ["Completed basic programming courses"],
#             "insights": ["Student is motivated and has clear goals"]
#         }
        
#         self.mock_summary_response = """
#         This session focused on Test Student's career aspirations in software development and machine learning. 
#         The student demonstrated clear motivation and has already completed foundational programming courses. 
#         Key action items include creating a structured study plan and applying for relevant internships.
#         """
        
#         self.mock_email_response = """
#         Dear Test Student,
        
#         Thank you for our productive career counseling session today. I enjoyed discussing your goals in software development and machine learning.
        
#         As we discussed, your next steps include creating a study plan and applying for internships. I'm confident you'll make great progress toward your career goals.
        
#         Please don't hesitate to reach out if you need any guidance along the way.
        
#         Best regards,
#         Dr. Test
#         """
    
#     @patch('counseling_agent.ChatGoogleGenerativeAI')
#     def test_extract_key_takeaways(self, mock_chat_gemini):
#         """Test key takeaways extraction."""
#         # Mock the LLM response
#         mock_llm = Mock()
#         mock_llm.invoke.return_value.content = json.dumps(self.mock_takeaways_response)
#         mock_chat_gemini.return_value = mock_llm
        
#         # Initialize agent
#         agent = CounselingSessionAgent()
        
#         # Test extraction
#         result = agent.extract_key_takeaways(self.sample_transcript.transcript)
        
#         # Verify results
#         self.assertIn("career_goals", result)
#         self.assertIn("action_items", result)
#         self.assertEqual(len(result["career_goals"]), 2)
#         self.assertEqual(len(result["action_items"]), 2)
    
#     @patch('counseling_agent.ChatGoogleGenerativeAI')
#     def test_generate_session_summary(self, mock_chat_gemini):
#         """Test session summary generation."""
#         # Mock the LLM response
#         mock_llm = Mock()
#         mock_llm.invoke.return_value.content = self.mock_summary_response
#         mock_chat_gemini.return_value = mock_llm
        
#         # Initialize agent
#         agent = CounselingSessionAgent()
        
#         # Test summary generation
#         summary = agent.generate_session_summary(
#             self.sample_transcript, 
#             self.mock_takeaways_response
#         )
        
#         # Verify summary
#         self.assertEqual(summary.session_id, "test_session_001")
#         self.assertEqual(summary.student_name, "Test Student")
#         self.assertIsNotNone(summary.summary_text)
#         self.assertEqual(len(summary.career_goals), 2)
#         self.assertEqual(len(summary.action_items), 2)
    
#     @patch('counseling_agent.ChatGoogleGenerativeAI')
#     def test_generate_follow_up_email(self, mock_chat_gemini):
#         """Test follow-up email generation."""
#         # Mock the LLM response
#         mock_llm = Mock()
#         mock_llm.invoke.return_value.content = self.mock_email_response
#         mock_chat_gemini.return_value = mock_llm
        
#         # Initialize agent
#         agent = CounselingSessionAgent()
        
#         # Create a session summary
#         summary = agent.generate_session_summary(
#             self.sample_transcript, 
#             self.mock_takeaways_response
#         )
        
#         # Test email generation
#         email = agent.generate_follow_up_email(summary, "test@university.edu")
        
#         # Verify email
#         self.assertEqual(email.to_email, "test@university.edu")
#         self.assertIn("Follow-up", email.subject)
#         self.assertIsNotNone(email.body)
    
#     @patch('counseling_agent.ChatGoogleGenerativeAI')
#     def test_process_session_complete(self, mock_chat_gemini):
#         """Test complete session processing."""
#         # Mock the LLM responses
#         mock_llm = Mock()
#         mock_llm.invoke.side_effect = [
#             Mock(content=json.dumps(self.mock_takeaways_response)),
#             Mock(content=self.mock_summary_response),
#             Mock(content=self.mock_email_response)
#         ]
#         mock_chat_gemini.return_value = mock_llm
        
#         # Initialize agent
#         agent = CounselingSessionAgent()
        
#         # Test complete processing
#         result = agent.process_session(self.sample_transcript)
        
#         # Verify result
#         self.assertTrue(result.success)
#         self.assertIsNotNone(result.data["session_summary"])
#         self.assertIsNotNone(result.data["follow_up_email"])
#         self.assertIsNotNone(result.data["key_takeaways"])
    
#     def test_fallback_extraction(self):
#         """Test fallback extraction when JSON parsing fails."""
#         # Initialize agent
#         agent = CounselingSessionAgent()
        
#         # Test with malformed response
#         malformed_response = """
#         Career Goals:
#         - Work in software development
#         - Learn machine learning
        
#         Action Items:
#         - Create study plan
#         - Apply for internships
#         """
        
#         result = agent._fallback_extraction(malformed_response)
        
#         # Verify fallback extraction
#         self.assertIn("career_goals", result)
#         self.assertIn("action_items", result)
#         self.assertTrue(len(result["career_goals"]) > 0)
#         self.assertTrue(len(result["action_items"]) > 0)

# class TestDataModels(unittest.TestCase):
#     """Test cases for data models."""
    
#     def test_session_transcript_validation(self):
#         """Test SessionTranscript model validation."""
#         # Valid transcript
#         transcript = SessionTranscript(
#             session_id="test_001",
#             date=datetime.now(),
#             participants=[
#                 SessionParticipant(name="Dr. Test", role="counselor"),
#                 SessionParticipant(name="Student", role="student")
#             ],
#             transcript="Test transcript content"
#         )
        
#         self.assertEqual(transcript.session_id, "test_001")
#         self.assertEqual(len(transcript.participants), 2)
    
#     def test_session_participant_validation(self):
#         """Test SessionParticipant model validation."""
#         participant = SessionParticipant(
#             name="Test Student",
#             role="student",
#             email="test@university.edu"
#         )
        
#         self.assertEqual(participant.name, "Test Student")
#         self.assertEqual(participant.role, "student")
#         self.assertEqual(participant.email, "test@university.edu")

# def run_tests():
#     """Run all tests."""
#     print("🧪 Running Counseling Session Agent Tests (Gemini)")
#     print("=" * 50)
    
#     # Create test suite
#     test_suite = unittest.TestSuite()
    
#     # Add test cases
#     test_suite.addTest(unittest.makeSuite(TestCounselingSessionAgent))
#     test_suite.addTest(unittest.makeSuite(TestDataModels))
    
#     # Run tests
#     runner = unittest.TextTestRunner(verbosity=2)
#     result = runner.run(test_suite)
    
#     # Print summary
#     print("\n" + "=" * 50)
#     if result.wasSuccessful():
#         print("✅ All tests passed!")
#     else:
#         print("❌ Some tests failed!")
#         print(f"Failures: {len(result.failures)}")
#         print(f"Errors: {len(result.errors)}")
    
#     return result.wasSuccessful()

# if __name__ == "__main__":
#     run_tests() 