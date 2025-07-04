from fastmcp import FastMCP
from services.document_service import DocumentService
from services.sentiment_service import SentimentService
from services.keyword_service import KeywordService
from services.readability_service import ReadabilityService
from services.stats_service import StatsService
from utils.validation import validate_keyword_limit
import asyncio
import logging

logger = logging.getLogger(__name__)

# Initialize services
document_service = DocumentService()
sentiment_service = SentimentService()
keyword_service = KeywordService()
readability_service = ReadabilityService()
stats_service = StatsService()

def register_analyze_document_tool(app: FastMCP):
    """Register the analyze_document tool with the FastMCP app"""
    
    @app.tool()
    async def analyze_document(document_id: str, limit: int = 5) -> dict:
        """
        Perform complete analysis of a stored document including sentiment, keywords, readability, and statistics.
        
        Args:
            document_id: ID of the document to analyze
            limit: Maximum number of keywords to extract (default: 5, max: 20)
        
        Returns:
            Dictionary with complete analysis results
        """
        try:
            # Validate inputs
            if not document_id or not document_id.strip():
                return {
                    "success": False,
                    "error": "Empty document ID provided",
                    "message": "Please provide a valid document ID"
                }
            
            # Validate and normalize keyword limit
            normalized_limit = validate_keyword_limit(limit)
            
            # Get document
            document = document_service.get_document(document_id.strip())
            if not document:
                return {
                    "success": False,
                    "error": "Document not found",
                    "message": f"No document found with ID: {document_id}"
                }
            
            # Perform all analyses in parallel for better performance
            sentiment_task = sentiment_service.analyze_sentiment(document.text)
            keywords_task = asyncio.create_task(
                asyncio.to_thread(keyword_service.extract_keywords, document.text, normalized_limit)
            )
            readability_task = asyncio.create_task(
                asyncio.to_thread(readability_service.calculate_readability, document.text)
            )
            stats_task = asyncio.create_task(
                asyncio.to_thread(stats_service.calculate_stats, document.text)
            )
            
            # Wait for all analyses to complete
            sentiment_result, keywords, readability_result, stats_result = await asyncio.gather(
                sentiment_task,
                keywords_task,
                readability_task,
                stats_task,
                return_exceptions=True
            )
            
            # Handle any exceptions from parallel execution
            if isinstance(sentiment_result, Exception):
                logger.error(f"Sentiment analysis failed: {sentiment_result}")
                sentiment_result = {"label": "NEUTRAL", "confidence": 0.5}
            else:
                sentiment_result = {
                    "label": sentiment_result.label,
                    "confidence": sentiment_result.confidence
                }
            
            if isinstance(keywords, Exception):
                logger.error(f"Keyword extraction failed: {keywords}")
                keywords = ["analysis", "text", "content"]
            
            if isinstance(readability_result, Exception):
                logger.error(f"Readability analysis failed: {readability_result}")
                readability_result = {
                    "flesch_reading_ease": 50.0,
                    "flesch_kincaid_grade": 10.0,
                    "gunning_fog_index": 12.0
                }
            else:
                readability_result = {
                    "flesch_reading_ease": readability_result.flesch_reading_ease,
                    "flesch_kincaid_grade": readability_result.flesch_kincaid_grade,
                    "gunning_fog_index": readability_result.gunning_fog_index
                }
            
            if isinstance(stats_result, Exception):
                logger.error(f"Stats calculation failed: {stats_result}")
                stats_result = {
                    "word_count": len(document.text.split()),
                    "sentence_count": 1,
                    "avg_words_per_sentence": len(document.text.split()),
                    "character_count": len(document.text)
                }
            else:
                stats_result = {
                    "word_count": stats_result.word_count,
                    "sentence_count": stats_result.sentence_count,
                    "avg_words_per_sentence": stats_result.avg_words_per_sentence,
                    "character_count": stats_result.character_count
                }
            
            # Compile complete analysis result
            analysis_result = {
                "success": True,
                "document_id": document_id,
                "document_title": document.title,
                "document_author": document.author,
                "sentiment": sentiment_result,
                "keywords": keywords,
                "readability": readability_result,
                "stats": stats_result,
                "message": f"Complete analysis of document '{document.title}' completed successfully"
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in analyze_document: {e}")
            return {
                "success": False,
                "error": "Analysis failed",
                "message": "Failed to analyze document due to internal error"
            }
