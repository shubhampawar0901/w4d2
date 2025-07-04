import json
import os
from typing import List, Dict, Any, Optional
from models.document import Document
import uuid
from datetime import datetime

class DocumentStorage:
    """Handles document storage and retrieval from JSON file"""
    
    def __init__(self, file_path: str = "data/documents.json"):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the documents file if it doesn't exist"""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def load_documents(self) -> List[Document]:
        """Load all documents from the JSON file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Document(**doc) for doc in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_documents(self, documents: List[Document]):
        """Save all documents to the JSON file"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            data = [doc.model_dump() for doc in documents]
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """Get a specific document by ID"""
        documents = self.load_documents()
        for doc in documents:
            if doc.document_id == document_id:
                return doc
        return None
    
    def add_document(self, document_data: Dict[str, Any]) -> str:
        """Add a new document and return its ID"""
        documents = self.load_documents()
        
        # Generate unique ID
        document_id = f"doc_{str(uuid.uuid4())[:8]}"
        
        # Set creation date if not provided
        if 'created_at' not in document_data or not document_data['created_at']:
            document_data['created_at'] = datetime.now().strftime("%Y-%m-%d")
        
        # Create document with ID
        document_data['document_id'] = document_id
        new_document = Document(**document_data)
        
        # Add to list and save
        documents.append(new_document)
        self.save_documents(documents)
        
        return document_id
    
    def search_documents(self, query: str) -> List[Document]:
        """Search documents by title, author, or content"""
        documents = self.load_documents()
        query_lower = query.lower()
        
        matching_docs = []
        for doc in documents:
            if (query_lower in doc.title.lower() or 
                query_lower in doc.author.lower() or 
                query_lower in doc.text.lower() or
                query_lower in doc.category.lower()):
                matching_docs.append(doc)
        
        return matching_docs
