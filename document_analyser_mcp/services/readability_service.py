import textstat
from models.analysis import ReadabilityResult
import logging

logger = logging.getLogger(__name__)

class ReadabilityService:
    """Service for calculating readability metrics using textstat"""
    
    def __init__(self):
        # Set textstat language to English
        textstat.set_lang("en")
        logger.info("ReadabilityService initialized")
    
    def calculate_readability(self, text: str) -> ReadabilityResult:
        """Calculate various readability metrics for the given text"""
        try:
            # Calculate Flesch Reading Ease
            # Scale: 0-100 (higher = easier to read)
            # 90-100: Very Easy, 80-90: Easy, 70-80: Fairly Easy
            # 60-70: Standard, 50-60: Fairly Difficult, 30-50: Difficult, 0-30: Very Difficult
            flesch_ease = textstat.flesch_reading_ease(text)
            
            # Calculate Flesch-Kincaid Grade Level
            # Indicates the US grade level needed to understand the text
            flesch_kincaid = textstat.flesch_kincaid_grade(text)
            
            # Calculate Gunning Fog Index
            # Estimates years of formal education needed to understand text
            gunning_fog = textstat.gunning_fog(text)
            
            return ReadabilityResult(
                flesch_reading_ease=round(flesch_ease, 2),
                flesch_kincaid_grade=round(flesch_kincaid, 2),
                gunning_fog_index=round(gunning_fog, 2)
            )
            
        except Exception as e:
            logger.error(f"Readability calculation failed: {e}")
            # Return default values if calculation fails
            return ReadabilityResult(
                flesch_reading_ease=50.0,  # Standard difficulty
                flesch_kincaid_grade=10.0,  # 10th grade level
                gunning_fog_index=12.0     # 12 years education
            )
    
    def get_readability_interpretation(self, flesch_score: float) -> str:
        """Get human-readable interpretation of Flesch Reading Ease score"""
        if flesch_score >= 90:
            return "Very Easy (5th grade level)"
        elif flesch_score >= 80:
            return "Easy (6th grade level)"
        elif flesch_score >= 70:
            return "Fairly Easy (7th grade level)"
        elif flesch_score >= 60:
            return "Standard (8th-9th grade level)"
        elif flesch_score >= 50:
            return "Fairly Difficult (10th-12th grade level)"
        elif flesch_score >= 30:
            return "Difficult (college level)"
        else:
            return "Very Difficult (graduate level)"
