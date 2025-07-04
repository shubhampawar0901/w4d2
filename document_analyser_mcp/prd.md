Sure! Here's a clean and structured *Project Documentation (Doc)* for your *Document Analyzer MCP Server* built with fastmcp, containing *only descriptions and examples* — no source code.

---

# 📘 Document Analyzer MCP Server — Project Documentation

## 🧩 Overview

The *Document Analyzer MCP Server* is a Python-based microservice built using [fastmcp](https://pypi.org/project/fastmcp/). It exposes a set of tools that perform natural language processing (NLP) on text documents.

This service allows users to:

* Add documents
* Analyze them for sentiment, keywords, readability, and basic stats
* Search and retrieve documents
* Use NLP tools via a clean, modular MCP interface

---

## 🔧 Tech Stack

| Component          | Tool/Library                                        |
| ------------------ | --------------------------------------------------- |
| MCP Framework      | [fastmcp](https://pypi.org/project/fastmcp/)      |
| Web Framework      | FastAPI (under the hood)                            |
| NLP Utilities      | spaCy (en_core_web_sm)                            |
| Sentiment          | Hugging Face Transformers (e.g. BERT or DistilBERT) |
| Keyword Extraction | KeyBERT                                             |
| Readability        | textstat (Flesch, Gunning Fog)                      |
| Storage            | JSON file (flat document store)                     |

---

## 📁 Folder Structure (Overview)


document_analyzer/
├── main.py                  # MCP server setup
├── data/                    # Document storage
│   └── documents.json
├── tools/                   # MCP tools using @server.tool
│   ├── analyze_document.py
│   ├── add_document.py
│   ├── get_sentiment.py
│   ├── extract_keywords.py
│   ├── get_readability.py
│   ├── get_stats.py
│   └── search_documents.py
├── services/                # Tool logic (called by MCP tools)
├── models/                  # Pydantic schemas
├── utils/                   # spaCy loader, JSON helpers
└── requirements.txt


---

## 🧠 Available MCP Tools

### 1. add_document

Adds a new document with metadata (title, author, text).

*Example Input:*

json
{
  "title": "AI in Healthcare",
  "author": "Jane Doe",
  "text": "Artificial intelligence is transforming healthcare by improving diagnostics.",
  "created_at": "2025-07-04"
}


---

### 2. analyze_document

Performs a full analysis on a stored document by ID.

*Example Input:*

json
{
  "document_id": "doc_001",
  "limit": 5
}


*Example Output:*

json
{
  "sentiment": {"label": "POSITIVE", "confidence": 0.99},
  "keywords": ["ai", "healthcare", "diagnostics"],
  "readability": {
    "flesch_reading_ease": 47.5,
    "flesch_kincaid_grade": 10.3,
    "gunning_fog_index": 14.2
  },
  "stats": {
    "word_count": 139,
    "sentence_count": 5
  }
}


---

### 3. get_sentiment

Analyzes sentiment (positive, neutral, or negative) of any text.

*Example Input:*

json
{
  "text": "I really love the new design. It's clean and professional!"
}


*Example Output:*

json
{
  "label": "POSITIVE",
  "confidence": 0.985
}


---

### 4. extract_keywords

Extracts the top N keywords or phrases using BERT embeddings.

*Example Input:*

json
{
  "text": "AI is changing the world of healthcare and medical diagnostics.",
  "limit": 3
}


*Example Output:*

json
{
  "keywords": ["ai", "medical diagnostics", "healthcare"]
}


---

### 5. get_readability

Computes readability scores of the text.

*Example Input:*

json
{
  "text": "AI is transforming the way hospitals provide patient care."
}


*Example Output:*

json
{
  "flesch_reading_ease": 51.3,
  "flesch_kincaid_grade": 9.1,
  "gunning_fog_index": 13.4
}


---

### 6. get_stats

Returns word and sentence counts using spaCy.

*Example Input:*

json
{
  "text": "AI is evolving. It impacts diagnostics, treatment, and patient outcomes."
}


*Example Output:*

json
{
  "word_count": 13,
  "sentence_count": 3
}


---

### 7. search_documents

Searches stored documents by keyword or phrase.

*Example Input:*

json
{
  "query": "healthcare"
}


*Example Output:*

json
[
  {
    "document_id": "doc_001",
    "title": "AI in Healthcare",
    "matched": true
  }
]


---

## 🚀 How to Run the Server

1. Install dependencies:

bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm


2. Run the FastMCP server:

bash
uvicorn main:app --reload


3. Access your MCP tools:

* POST requests to /mcp/analyze_document
* All tools accessible under /mcp/*

---

## 📌 Notes

* You can test endpoints using Postman or cURL.
* Every MCP tool is modular and can be swapped or extended.
* Ideal for search indexing, tagging, and content summarization pipelines.

---

Let me know if you'd like this turned into a README.md or PDF for submission!