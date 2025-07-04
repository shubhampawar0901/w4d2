from typing import Optional
import re

def validate_text_length(text: str, max_length: int = 10000) -> bool:
    """Validate text length is within acceptable limits"""
    return len(text) <= max_length

def validate_document_id(document_id: str) -> bool:
    """Validate document ID format"""
    pattern = r'^doc_[a-zA-Z0-9]{8}$'
    return bool(re.match(pattern, document_id))

def sanitize_text(text: str) -> str:
    """Basic text sanitization"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def validate_keyword_limit(limit: int) -> int:
    """Validate and normalize keyword limit"""
    if limit < 1:
        return 1
    if limit > 20:
        return 20
    return limit

def validate_date_format(date_str: str) -> bool:
    """Validate date format YYYY-MM-DD"""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_str))
