# W4D2 - MCP Server Projects

This repository contains two sophisticated MCP (Model Context Protocol) server implementations for Week 4, Day 2 assignment.

## 📚 Project 1: Document Analyzer MCP Server

A comprehensive document analysis system with AI-powered text processing capabilities.

### Features
- **Sentiment Analysis**: Positive/negative/neutral sentiment detection using Hugging Face API
- **Keyword Extraction**: Intelligent keyword extraction using KeyBERT
- **Readability Scoring**: Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog Index
- **Document Storage**: 20+ sample AI-related documents with metadata
- **Search Functionality**: Content-based document search

### MCP Tools
1. `add_document` - Store new documents with metadata
2. `analyze_document` - Full analysis (sentiment + keywords + readability + stats)
3. `get_sentiment` - Sentiment analysis only
4. `extract_keywords` - Keyword extraction only
5. `search_documents` - Search functionality

### Tech Stack
- **FastMCP**: MCP framework with FastAPI
- **Hugging Face API**: Sentiment analysis
- **KeyBERT**: Keyword extraction
- **textstat**: Readability scoring
- **spaCy**: Text processing and statistics

### Sample Documents
20 comprehensive AI-related documents covering:
- Healthcare AI, Machine Learning, Ethics
- NLP, Computer Vision, Robotics
- Deep Learning, Finance AI, Autonomous Vehicles
- Climate AI, Quantum Computing, Education
- Generative AI, AI Safety, Future of Work
- Product Reviews, News Articles, Creative Writing

## 🤖 Project 2: Smart Meeting Assistant MCP Server

An AI-powered meeting scheduling and management system with intelligent optimization.

### Features
- **Intelligent Scheduling**: AI-powered conflict detection and resolution
- **Optimal Time Recommendations**: Multi-factor scoring for best meeting times
- **Meeting Analytics**: Pattern analysis and productivity insights
- **Workload Balancing**: Team meeting load distribution
- **Agenda Generation**: Smart agenda suggestions using NLP
- **Effectiveness Scoring**: Meeting productivity assessment

### MCP Tools
1. `create_meeting` - Schedule new meetings with conflict checking
2. `find_optimal_slots` - AI-powered time recommendations
3. `detect_scheduling_conflicts` - Advanced conflict detection
4. `analyze_meeting_patterns` - Meeting behavior analysis
5. `generate_agenda_suggestions` - Smart agenda creation
6. `calculate_workload_balance` - Team workload analysis
7. `score_meeting_effectiveness` - Productivity assessment
8. `optimize_meeting_schedule` - Schedule optimization

### AI Features
- **Multi-factor Scoring**: Productivity (40%) + Convenience (30%) + Conflict Risk (20%) + Preferences (10%)
- **Time Zone Intelligence**: Global scheduling with fairness algorithms
- **Pattern Recognition**: Learning from meeting history
- **Predictive Scheduling**: Anticipating future conflicts

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Hugging Face API token
- FastMCP framework

### Installation

1. Clone the repository:
```bash
git clone https://github.com/shubhampawar0901/w4d2.git
cd w4d2
```

2. Install dependencies for Document Analyzer:
```bash
cd document_analyser_mcp
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file with your Hugging Face token
echo "HUGGINGFACE_API_TOKEN=your_token_here" > .env
```

4. Run the Document Analyzer server:
```bash
python main.py
```

### Usage Examples

**Document Analysis:**
```python
# Analyze a document
result = analyze_document("doc_001", limit=5)

# Get sentiment only
sentiment = get_sentiment("This is a great product!")

# Extract keywords
keywords = extract_keywords("AI and machine learning are transforming healthcare", limit=3)
```

**Meeting Scheduling:**
```python
# Find optimal meeting slots
slots = find_optimal_slots(
    participants=["user_001", "user_002", "user_003"],
    duration=60,
    date_range=["2024-12-16", "2024-12-20"]
)

# Create a meeting
meeting = create_meeting(
    title="Team Standup",
    participants=["user_001", "user_002"],
    duration=30,
    preferences={"time_zone": "America/New_York"}
)
```

## 📊 Project Statistics

### Document Analyzer
- **20 Documents**: 4,933 words total
- **5 MCP Tools**: Complete text analysis pipeline
- **Multiple Categories**: Technical, ethical, industry applications
- **Rich Test Data**: Perfect for testing all analysis features

### Meeting Assistant
- **8 MCP Tools**: Comprehensive meeting management
- **AI Scheduling Engine**: Multi-factor optimization
- **60+ Sample Meetings**: Realistic corporate scenarios
- **Global Support**: Multi-timezone intelligence

## 🏗️ Architecture

Both projects follow clean architecture principles:
- **MCP Tools Layer**: User-facing tool interfaces
- **Services Layer**: Business logic and AI processing
- **Models Layer**: Pydantic data validation
- **Storage Layer**: JSON-based data persistence

## 🔮 Future Enhancements

### Document Analyzer
- Real-time document processing
- Multi-language support
- Advanced NLP features
- Integration with document management systems

### Meeting Assistant
- Calendar API integration (Google/Outlook)
- Real-time notifications
- Video conferencing integration
- Advanced analytics dashboard

## 📝 License

This project is part of an educational assignment and is intended for learning purposes.

## 👥 Contributors

- **Student**: Implementation and development
- **Augment Agent**: AI-assisted development and architecture design

---

**Note**: This repository demonstrates advanced MCP server development with AI integration, showcasing both text analysis and intelligent scheduling capabilities.
