from typing import List, Optional, Dict, Any
from models.document import Document, DocumentCreate, DocumentSummary
from utils.file_utils import DocumentStorage
from utils.validation import validate_text_length, sanitize_text
import logging

logger = logging.getLogger(__name__)

class DocumentService:
    """Service for document management operations"""
    
    def __init__(self, storage_path: str = "data/documents.json"):
        self.storage = DocumentStorage(storage_path)
        logger.info("DocumentService initialized")
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """Retrieve a document by its ID"""
        try:
            return self.storage.get_document(document_id)
        except Exception as e:
            logger.error(f"Failed to get document {document_id}: {e}")
            return None
    
    def add_document(self, document_data: DocumentCreate) -> str:
        """Add a new document and return its ID"""
        try:
            # Validate text length
            if not validate_text_length(document_data.text):
                raise ValueError("Text exceeds maximum length limit")
            
            # Sanitize text content
            sanitized_text = sanitize_text(document_data.text)
            
            # Prepare document data
            doc_dict = {
                "title": document_data.title.strip(),
                "author": document_data.author.strip(),
                "text": sanitized_text,
                "category": document_data.category.strip(),
                "created_at": document_data.created_at
            }
            
            # Add document to storage
            document_id = self.storage.add_document(doc_dict)
            logger.info(f"Document added successfully with ID: {document_id}")
            
            return document_id
            
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            raise
    
    def search_documents(self, query: str) -> List[DocumentSummary]:
        """Search documents and return summaries"""
        try:
            if not query.strip():
                return []
            
            matching_docs = self.storage.search_documents(query)
            
            # Convert to summary format
            summaries = []
            for doc in matching_docs:
                summary = DocumentSummary(
                    document_id=doc.document_id,
                    title=doc.title,
                    author=doc.author,
                    category=doc.category,
                    matched=True
                )
                summaries.append(summary)
            
            logger.info(f"Found {len(summaries)} documents matching query: {query}")
            return summaries
            
        except Exception as e:
            logger.error(f"Search failed for query '{query}': {e}")
            return []
    
    def get_all_documents(self) -> List[DocumentSummary]:
        """Get summaries of all documents"""
        try:
            all_docs = self.storage.load_documents()
            summaries = []
            
            for doc in all_docs:
                summary = DocumentSummary(
                    document_id=doc.document_id,
                    title=doc.title,
                    author=doc.author,
                    category=doc.category
                )
                summaries.append(summary)
            
            return summaries
            
        except Exception as e:
            logger.error(f"Failed to get all documents: {e}")
            return []
