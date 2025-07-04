from fastmcp import FastMCP
from services.sentiment_service import SentimentService
from utils.validation import validate_text_length, sanitize_text
import logging

logger = logging.getLogger(__name__)

# Initialize services
sentiment_service = SentimentService()

def register_get_sentiment_tool(app: FastMCP):
    """Register the get_sentiment tool with the FastMCP app"""
    
    @app.tool()
    async def get_sentiment(text: str) -> dict:
        """
        Analyze sentiment of the provided text.
        
        Args:
            text: Text to analyze for sentiment
        
        Returns:
            Dictionary with sentiment label and confidence score
        """
        try:
            # Validate and sanitize input
            if not text or not text.strip():
                return {
                    "success": False,
                    "error": "Empty text provided",
                    "message": "Please provide text to analyze"
                }
            
            if not validate_text_length(text):
                return {
                    "success": False,
                    "error": "Text too long",
                    "message": "Text exceeds maximum length limit"
                }
            
            # Sanitize text
            clean_text = sanitize_text(text)
            
            # Perform sentiment analysis
            sentiment_result = await sentiment_service.analyze_sentiment(clean_text)
            
            return {
                "success": True,
                "label": sentiment_result.label,
                "confidence": sentiment_result.confidence,
                "message": f"Sentiment analysis completed: {sentiment_result.label} ({sentiment_result.confidence:.3f})"
            }
            
        except Exception as e:
            logger.error(f"Error in get_sentiment: {e}")
            return {
                "success": False,
                "error": "Analysis failed",
                "message": "Failed to analyze sentiment due to internal error"
            }
