# 🤖 Counseling Session Agent

An AI-powered agent that processes counseling session transcripts to automatically generate session summaries and personalized follow-up emails for students.

## 🎯 Features

- **Intelligent Transcript Analysis**: Uses Google Gemini to extract key takeaways from counseling conversations
- **Automated Summary Generation**: Creates professional session summaries with career goals, action items, and insights
- **Personalized Email Creation**: Generates friendly, action-oriented follow-up emails
- **Email Integration**: Supports both real SMTP sending and mock email functionality for testing
- **Transcript File Input**: Reads the transcript from a user-editable file (e.g., transcript.txt or transcript2.txt)
- **Automatic Student Name Extraction**: The agent auto-detects the student's name from the transcript
- **User Prompt for Email Saving**: Prompts the user before saving any follow-up email template to avoid spamming
- **REST API**: FastAPI-based web service for easy integration
- **Modular Architecture**: Clean, extensible codebase with proper separation of concerns

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key
- (Optional) SMTP credentials for email sending

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd counseling-session-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   # Required
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Optional - for real email sending
   SMTP_SERVER=smtp.mailslurp.com
   SMTP_PORT=587
   SMTP_USERNAME=your_mailslurp_username
   SMTP_PASSWORD=your_mailslurp_password
   
   # Application settings
   DEBUG=True
   LOG_LEVEL=INFO
   ```

4. **Prepare your transcript**
   - Edit `transcript.txt` (or another file, e.g., `transcript2.txt`) and paste your counseling session conversation there.
   - The agent will automatically extract the student's name from the transcript.

5. **Run the demo**
   ```bash
   python example_usage.py
   ```
   - The script will process the transcript, display the summary and key takeaways, and prompt you before saving any follow-up email template.

## 📖 Usage

### Basic Usage

- Edit your transcript in `transcript.txt` (or change the filename in `example_usage.py` if desired).
- Run the script:
  ```bash
  python example_usage.py
  ```
- The agent will:
  1. Read the transcript from the file
  2. Auto-detect the student's name
  3. Extract key takeaways (career goals, action items)
  4. Generate a session summary
  5. Generate a follow-up email (mock send)
  6. Prompt you before saving the email template

### Customizing Participants
- The student's name is auto-extracted from the transcript (first non-counselor speaker).
- The counselor's name/email can be edited in `example_usage.py` if needed.

### API Usage

1. **Start the API server**
   ```bash
   python api.py
   ```

2. **Make API requests**
   ```bash
   # Process a session
   curl -X POST "http://localhost:8000/process-session" \
        -H "Content-Type: application/json" \
        -d @session_data.json
   
   # Extract takeaways only
   curl -X POST "http://localhost:8000/extract-takeaways" \
        -H "Content-Type: application/json" \
        -d '{"transcript": "Your transcript here..."}'
   ```

## 🏗️ Architecture

### Core Components

- **`CounselingSessionAgent`**: Main AI agent that processes transcripts
- **`EmailService`**: Handles email sending (real or mock)
- **`models.py`**: Pydantic models for data validation
- **`api.py`**: FastAPI web service
- **`config.py`**: Configuration management

### Data Flow

1. **Input**: Counseling session transcript from a file (with participant information auto-extracted)
2. **Processing**: 
   - Extract key takeaways using Gemini LLM
   - Generate session summary
   - Create personalized follow-up email
3. **Output**: Structured summary and email content
4. **Delivery**: Optionally save email template (user prompted)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `GEMINI_MODEL` | Gemini model to use | No | `gemini-2.0-flash` |
| `SMTP_SERVER` | SMTP server for emails | No | `smtp.mailslurp.com` |
| `SMTP_PORT` | SMTP port | No | `587` |
| `SMTP_USERNAME` | SMTP username | No | - |
| `SMTP_PASSWORD` | SMTP password | No | - |
| `DEBUG` | Enable debug mode | No | `True` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

### Email Configuration

The system supports two email modes:

1. **Mock Mode** (default): Logs emails to console without sending
2. **Real SMTP**: Sends actual emails using configured SMTP server

To enable real email sending, configure your SMTP credentials in the `.env` file.

## 🧪 Testing

### Running the Demo

```bash
python example_usage.py
```

This will:
1. Read your transcript from file
2. Process it through the AI agent
3. Display the generated summary and key takeaways
4. Generate a follow-up email (mock send)
5. Prompt you before saving the email template

## 📁 Project Structure

```
counseling-session-agent/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── config.py                # Configuration management
├── models.py                # Pydantic data models
├── counseling_agent.py      # Main AI agent
├── email_service.py         # Email handling service
├── api.py                   # FastAPI web service
├── example_usage.py         # Demo script
├── transcript.txt           # Your counseling session transcript
├── emails/                  # Generated email templates (if saved)
```

## 🔍 Key Features Explained

### Intelligent Transcript Analysis

The agent uses carefully crafted prompts to extract:
- Career goals and aspirations
- Action items and next steps

### Personalized Email Generation

Follow-up emails are:
- Personalized with the student's name (auto-extracted)
- Action-oriented with specific next steps
- Encouraging and supportive in tone
- Professional yet friendly
- Structured for clarity

### Error Handling

The system includes robust error handling:
- Graceful fallbacks for LLM parsing issues
- Mock email functionality when SMTP is unavailable
- Comprehensive logging for debugging
- Input validation using Pydantic models

## 🚀 Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the API server
python api.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the documentation
2. Review the example usage
3. Open an issue on GitHub

## 🎓 Learning Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/) 
