from fastmcp import FastMCP
from models.document import DocumentCreate
from services.document_service import DocumentService
import logging

logger = logging.getLogger(__name__)

# Initialize services
document_service = DocumentService()

def register_add_document_tool(app: FastMCP):
    """Register the add_document tool with the FastMCP app"""
    
    @app.tool()
    async def add_document(
        title: str,
        author: str,
        text: str,
        created_at: str = None,
        category: str = "general"
    ) -> dict:
        """
        Add a new document to the storage system.
        
        Args:
            title: Document title
            author: Document author
            text: Document content text
            created_at: Creation date (YYYY-MM-DD format, auto-generated if not provided)
            category: Document category (default: "general")
        
        Returns:
            Dictionary with document_id and success message
        """
        try:
            # Create document data object
            document_data = DocumentCreate(
                title=title,
                author=author,
                text=text,
                created_at=created_at,
                category=category
            )
            
            # Add document using service
            document_id = document_service.add_document(document_data)
            
            return {
                "success": True,
                "document_id": document_id,
                "message": f"Document '{title}' added successfully with ID: {document_id}"
            }
            
        except ValueError as e:
            logger.error(f"Validation error in add_document: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to add document due to validation error"
            }
        except Exception as e:
            logger.error(f"Error in add_document: {e}")
            return {
                "success": False,
                "error": "Internal server error",
                "message": "Failed to add document due to internal error"
            }
