import requests
import asyncio
from typing import Dict, Any
from models.analysis import SentimentResult
from config import Config
import logging

logger = logging.getLogger(__name__)

class SentimentService:
    """Service for sentiment analysis using Hugging Face API"""
    
    def __init__(self):
        self.api_key = Config.HUGGING_FACE_API_KEY
        self.api_url = Config.get_sentiment_api_url()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def analyze_sentiment(self, text: str) -> SentimentResult:
        """Analyze sentiment of the given text"""
        try:
            # Prepare the request
            payload = {"inputs": text}
            
            # Make async request to Hugging Face API
            response = await self._make_request(payload)
            
            # Parse response
            if response and len(response) > 0:
                # Get the highest confidence prediction
                predictions = response[0]
                best_prediction = max(predictions, key=lambda x: x['score'])
                
                # Map label to standard format
                label = self._normalize_label(best_prediction['label'])
                confidence = best_prediction['score']
                
                return SentimentResult(label=label, confidence=confidence)
            else:
                # Fallback to neutral if API fails
                return SentimentResult(label="NEUTRAL", confidence=0.5)
                
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            # Return neutral sentiment as fallback
            return SentimentResult(label="NEUTRAL", confidence=0.5)
    
    async def _make_request(self, payload: Dict[str, Any]) -> Any:
        """Make async HTTP request to Hugging Face API"""
        loop = asyncio.get_event_loop()
        
        def make_sync_request():
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=Config.API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        
        return await loop.run_in_executor(None, make_sync_request)
    
    def _normalize_label(self, label: str) -> str:
        """Normalize sentiment labels to standard format"""
        label_upper = label.upper()
        
        # Map various label formats to standard ones
        if 'POSITIVE' in label_upper or 'POS' in label_upper:
            return "POSITIVE"
        elif 'NEGATIVE' in label_upper or 'NEG' in label_upper:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
