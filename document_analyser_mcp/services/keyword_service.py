from keybert import KeyBERT
from typing import List
import logging

logger = logging.getLogger(__name__)

class KeywordService:
    """Service for keyword extraction using KeyBERT"""
    
    def __init__(self):
        try:
            # Initialize KeyBERT with sentence-transformers model
            self.kw_model = KeyBERT()
            logger.info("KeyBERT model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize KeyBERT: {e}")
            self.kw_model = None
    
    def extract_keywords(self, text: str, limit: int = 5) -> List[str]:
        """Extract keywords from the given text"""
        try:
            if not self.kw_model:
                # Fallback to simple word frequency if KeyBERT fails
                return self._fallback_keyword_extraction(text, limit)
            
            # Use KeyBERT to extract keywords
            keywords = self.kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),  # Extract 1-2 word phrases
                stop_words='english',
                use_maxsum=True,  # Use Max Sum Similarity for diversity
                nr_candidates=20  # Consider top 20 candidates
            )

            # Limit the results
            keywords = keywords[:limit]
            
            # Extract just the keyword strings (not scores)
            keyword_list = [kw[0] for kw in keywords]
            
            return keyword_list
            
        except Exception as e:
            logger.error(f"Keyword extraction failed: {e}")
            return self._fallback_keyword_extraction(text, limit)
    
    def _fallback_keyword_extraction(self, text: str, limit: int) -> List[str]:
        """Simple fallback keyword extraction using word frequency"""
        try:
            import re
            from collections import Counter
            
            # Simple preprocessing
            text = text.lower()
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text)  # Words with 3+ letters
            
            # Common stop words to filter out
            stop_words = {
                'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
                'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
                'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these',
                'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
                'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
                'may', 'might', 'must', 'can', 'shall', 'not', 'no', 'yes', 'all',
                'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such'
            }
            
            # Filter out stop words
            filtered_words = [word for word in words if word not in stop_words]
            
            # Count word frequency
            word_counts = Counter(filtered_words)
            
            # Get top keywords
            top_keywords = [word for word, count in word_counts.most_common(limit)]
            
            return top_keywords
            
        except Exception as e:
            logger.error(f"Fallback keyword extraction failed: {e}")
            return ["analysis", "text", "content"]  # Default keywords
