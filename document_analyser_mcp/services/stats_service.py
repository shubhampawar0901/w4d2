import spacy
from models.analysis import StatsResult
import logging
import re

logger = logging.getLogger(__name__)

class StatsService:
    """Service for calculating text statistics using spaCy"""
    
    def __init__(self):
        try:
            # Load English language model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning("spaCy en_core_web_sm model not found, using fallback methods")
            self.nlp = None
    
    def calculate_stats(self, text: str) -> StatsResult:
        """Calculate text statistics for the given text"""
        try:
            if self.nlp:
                return self._calculate_with_spacy(text)
            else:
                return self._calculate_fallback(text)
                
        except Exception as e:
            logger.error(f"Stats calculation failed: {e}")
            return self._calculate_fallback(text)
    
    def _calculate_with_spacy(self, text: str) -> StatsResult:
        """Calculate stats using spaCy NLP model"""
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Count words (excluding punctuation and whitespace)
        word_count = len([token for token in doc if not token.is_punct and not token.is_space])
        
        # Count sentences
        sentence_count = len(list(doc.sents))
        
        # Calculate average words per sentence
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # Character count (excluding whitespace)
        character_count = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
        
        return StatsResult(
            word_count=word_count,
            sentence_count=sentence_count,
            avg_words_per_sentence=round(avg_words_per_sentence, 2),
            character_count=character_count
        )
    
    def _calculate_fallback(self, text: str) -> StatsResult:
        """Fallback stats calculation without spaCy"""
        # Simple word counting (split by whitespace, filter empty strings)
        words = [word for word in text.split() if word.strip()]
        word_count = len(words)
        
        # Simple sentence counting (count sentence-ending punctuation)
        sentence_endings = re.findall(r'[.!?]+', text)
        sentence_count = len(sentence_endings) if sentence_endings else 1
        
        # Calculate average words per sentence
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # Character count (excluding whitespace)
        character_count = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
        
        return StatsResult(
            word_count=word_count,
            sentence_count=sentence_count,
            avg_words_per_sentence=round(avg_words_per_sentence, 2),
            character_count=character_count
        )
