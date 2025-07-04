# 📘 Document Analyzer MCP Server

A comprehensive **FastMCP server** for document analysis featuring sentiment analysis, keyword extraction, readability scoring, and text statistics.

## 🚀 Features

### 🔍 **5 MCP Tools Available**
1. **`add_document`** - Store documents with metadata
2. **`analyze_document`** - Complete analysis (sentiment + keywords + readability + stats)
3. **`get_sentiment`** - Sentiment analysis for any text
4. **`extract_keywords`** - Keyword extraction for any text
5. **`search_documents`** - Search stored documents

### 🧠 **Analysis Capabilities**
- **Sentiment Analysis**: POSITIVE/NEGATIVE/NEUTRAL classification with confidence scores
- **Keyword Extraction**: Top relevant terms using KeyBERT and BERT embeddings
- **Readability Scoring**: Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog Index
- **Text Statistics**: Word count, sentence count, character count, averages

### 🔧 **Technology Stack**
- **FastMCP**: MCP framework with FastAPI
- **Hugging Face API**: Sentiment analysis (no local models)
- **KeyBERT**: Advanced keyword extraction
- **textstat**: Readability metrics
- **spaCy**: Text processing and statistics
- **JSON Storage**: Simple file-based document storage

## 📦 Installation

### Prerequisites
- Python 3.8+
- Hugging Face API token

### Quick Setup
```bash
# 1. Clone/navigate to the project directory
cd document_analyser_mcp

# 2. Run the setup script
python setup.py

# 3. Verify your .env file contains your Hugging Face token:
# HUGGING_FACE_API_KEY=hf_your_token_here

# 4. Start the server
python main.py
```

### Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file with your Hugging Face API key
echo "HUGGING_FACE_API_KEY=hf_your_token_here" > .env
```

## 🎯 Usage Examples

### Add a Document
```python
# MCP Tool Call
add_document(
    title="AI in Healthcare",
    author="Dr. Smith",
    text="Artificial intelligence is transforming healthcare...",
    category="healthcare"
)
```

### Complete Document Analysis
```python
# MCP Tool Call
analyze_document(
    document_id="doc_12345678",
    limit=5
)

# Returns:
{
    "sentiment": {"label": "POSITIVE", "confidence": 0.89},
    "keywords": ["artificial intelligence", "healthcare", "diagnostics"],
    "readability": {
        "flesch_reading_ease": 47.5,
        "flesch_kincaid_grade": 10.3,
        "gunning_fog_index": 14.2
    },
    "stats": {
        "word_count": 139,
        "sentence_count": 5,
        "avg_words_per_sentence": 27.8,
        "character_count": 1205
    }
}
```

### Sentiment Analysis
```python
get_sentiment(text="I love this new AI technology!")
# Returns: {"label": "POSITIVE", "confidence": 0.95}
```

### Keyword Extraction
```python
extract_keywords(
    text="Machine learning algorithms analyze data patterns",
    limit=3
)
# Returns: {"keywords": ["machine learning", "algorithms", "data patterns"]}
```

### Search Documents
```python
search_documents(query="healthcare")
# Returns list of matching documents
```

## 📁 Project Structure

```
document_analyzer/
├── main.py                    # FastMCP server entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
├── setup.py                   # Installation script
├── data/
│   └── documents.json         # Document storage (20 sample docs included)
├── models/                    # Pydantic schemas
│   ├── document.py           # Document models
│   └── analysis.py           # Analysis result models
├── services/                  # Business logic
│   ├── sentiment_service.py  # Hugging Face integration
│   ├── keyword_service.py    # KeyBERT implementation
│   ├── readability_service.py # textstat integration
│   ├── stats_service.py      # spaCy text processing
│   └── document_service.py   # Document management
├── tools/                     # MCP tool definitions
│   ├── add_document.py
│   ├── analyze_document.py
│   ├── get_sentiment.py
│   ├── extract_keywords.py
│   └── search_documents.py
└── utils/                     # Helper functions
    ├── file_utils.py         # JSON storage operations
    └── validation.py         # Input validation
```

## 📊 Sample Data

The server comes with **20 comprehensive AI-related documents** covering:
- Healthcare AI, Machine Learning, Ethics
- NLP, Computer Vision, Robotics
- Deep Learning, Finance, Autonomous Vehicles
- Climate AI, Quantum Computing, Education
- Generative AI, AI Safety, Future of Work
- Product reviews, news articles, creative writing

## 🔧 Configuration

### Environment Variables (.env)
```bash
HUGGING_FACE_API_KEY=hf_your_token_here
HUGGING_FACE_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
HUGGING_FACE_API_URL=https://api-inference.huggingface.co/models
```

### Server Settings (config.py)
- API timeout: 30 seconds
- Max text length: 10,000 characters
- Default keyword limit: 5
- Max keyword limit: 20

## 🧪 Testing

Start the server and test with any MCP client:

```bash
# Start server
python main.py

# Server runs on http://localhost:8000
# MCP tools available at /mcp/* endpoints
```

## 🚨 Error Handling

The server includes comprehensive error handling:
- Graceful API failures with fallback responses
- Input validation and sanitization
- Detailed logging for debugging
- User-friendly error messages

## 📝 License

This project is created for educational purposes as part of an AI/MCP learning assignment.

---

**Ready to analyze documents with AI? Start the server and connect your MCP client!** 🚀
