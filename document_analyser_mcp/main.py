#!/usr/bin/env python3
"""
Document Analyzer MCP Server

A FastMCP server that provides document analysis capabilities including:
- Sentiment analysis using Hugging Face API
- Keyword extraction using KeyBERT
- Readability scoring using textstat
- Text statistics using spaCy
- Document storage and search functionality

Author: AI Assistant
Date: 2024-12-15
"""

import logging
import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from fastmcp import FastMCP
from tools.add_document import register_add_document_tool
from tools.analyze_document import register_analyze_document_tool
from tools.get_sentiment import register_get_sentiment_tool
from tools.extract_keywords import register_extract_keywords_tool
from tools.search_documents import register_search_documents_tool
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('document_analyzer.log')
    ]
)

logger = logging.getLogger(__name__)

def create_app() -> FastMCP:
    """Create and configure the FastMCP application"""
    
    # Initialize FastMCP app
    app = FastMCP("Document Analyzer MCP Server")
    
    # Add description and metadata
    app.description = """
    Document Analyzer MCP Server provides comprehensive text analysis capabilities:
    
    🔍 Available Tools:
    - add_document: Store new documents with metadata
    - analyze_document: Complete analysis (sentiment + keywords + readability + stats)
    - get_sentiment: Sentiment analysis for any text
    - extract_keywords: Keyword extraction for any text
    - search_documents: Search stored documents
    
    🧠 Analysis Features:
    - Sentiment Analysis: Positive/Negative/Neutral classification
    - Keyword Extraction: Top relevant terms and phrases
    - Readability Scoring: Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog Index
    - Text Statistics: Word count, sentence count, averages
    
    🔧 Powered by:
    - Hugging Face API for sentiment analysis
    - KeyBERT for keyword extraction
    - textstat for readability metrics
    - spaCy for text processing
    """
    
    # Register all MCP tools
    logger.info("Registering MCP tools...")
    
    try:
        register_add_document_tool(app)
        logger.info("+ add_document tool registered")

        register_analyze_document_tool(app)
        logger.info("+ analyze_document tool registered")

        register_get_sentiment_tool(app)
        logger.info("+ get_sentiment tool registered")

        register_extract_keywords_tool(app)
        logger.info("+ extract_keywords tool registered")

        register_search_documents_tool(app)
        logger.info("+ search_documents tool registered")
        
        logger.info("All MCP tools registered successfully!")
        
    except Exception as e:
        logger.error(f"Failed to register tools: {e}")
        raise
    
    return app

def main():
    """Main entry point for the application"""
    try:
        logger.info("Starting Document Analyzer MCP Server...")
        
        # Validate configuration
        if not Config.HUGGING_FACE_API_KEY:
            logger.error("HUGGING_FACE_API_KEY not found in environment variables")
            sys.exit(1)
        
        # Create the app
        app = create_app()
        
        logger.info("Document Analyzer MCP Server initialized successfully!")
        logger.info("Available tools: add_document, analyze_document, get_sentiment, extract_keywords, search_documents")
        
        return app
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

# Create the app instance
app = main()

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    logger.info("Starting FastMCP server on http://localhost:8000")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
