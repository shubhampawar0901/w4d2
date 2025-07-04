from fastmcp import FastMCP
from services.keyword_service import KeywordService
from utils.validation import validate_text_length, validate_keyword_limit, sanitize_text
import logging

logger = logging.getLogger(__name__)

# Initialize services
keyword_service = KeywordService()

def register_extract_keywords_tool(app: FastMCP):
    """Register the extract_keywords tool with the FastMCP app"""
    
    @app.tool()
    async def extract_keywords(text: str, limit: int = 5) -> dict:
        """
        Extract keywords from the provided text.
        
        Args:
            text: Text to extract keywords from
            limit: Maximum number of keywords to extract (default: 5, max: 20)
        
        Returns:
            Dictionary with extracted keywords list
        """
        try:
            # Validate and sanitize input
            if not text or not text.strip():
                return {
                    "success": False,
                    "error": "Empty text provided",
                    "message": "Please provide text to extract keywords from"
                }
            
            if not validate_text_length(text):
                return {
                    "success": False,
                    "error": "Text too long",
                    "message": "Text exceeds maximum length limit"
                }
            
            # Validate and normalize limit
            normalized_limit = validate_keyword_limit(limit)
            
            # Sanitize text
            clean_text = sanitize_text(text)
            
            # Extract keywords
            keywords = keyword_service.extract_keywords(clean_text, normalized_limit)
            
            return {
                "success": True,
                "keywords": keywords,
                "count": len(keywords),
                "message": f"Extracted {len(keywords)} keywords successfully"
            }
            
        except Exception as e:
            logger.error(f"Error in extract_keywords: {e}")
            return {
                "success": False,
                "error": "Extraction failed",
                "message": "Failed to extract keywords due to internal error"
            }
