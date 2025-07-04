from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SentimentResult(BaseModel):
    """Sentiment analysis result"""
    label: str = Field(..., description="Sentiment label: POSITIVE, NEGATIVE, or NEUTRAL")
    confidence: float = Field(..., description="Confidence score between 0 and 1")

class ReadabilityResult(BaseModel):
    """Readability analysis result"""
    flesch_reading_ease: float = Field(..., description="Flesch Reading Ease score")
    flesch_kincaid_grade: float = Field(..., description="Flesch-Kincaid Grade Level")
    gunning_fog_index: float = Field(..., description="Gunning Fog Index")

class StatsResult(BaseModel):
    """Text statistics result"""
    word_count: int = Field(..., description="Total number of words")
    sentence_count: int = Field(..., description="Total number of sentences")
    avg_words_per_sentence: float = Field(..., description="Average words per sentence")
    character_count: int = Field(..., description="Total character count")

class KeywordResult(BaseModel):
    """Keyword extraction result"""
    keywords: List[str] = Field(..., description="List of extracted keywords")

class AnalysisResult(BaseModel):
    """Complete document analysis result"""
    document_id: str = Field(..., description="Document identifier")
    sentiment: SentimentResult = Field(..., description="Sentiment analysis results")
    keywords: List[str] = Field(..., description="Extracted keywords")
    readability: ReadabilityResult = Field(..., description="Readability metrics")
    stats: StatsResult = Field(..., description="Text statistics")

class TextAnalysisRequest(BaseModel):
    """Request model for text analysis"""
    text: str = Field(..., description="Text to analyze")
    limit: int = Field(default=5, description="Maximum number of keywords to extract")
