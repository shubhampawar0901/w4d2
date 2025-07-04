from fastmcp import FastMCP
from services.document_service import DocumentService
import logging

logger = logging.getLogger(__name__)

# Initialize services
document_service = DocumentService()

def register_search_documents_tool(app: FastMCP):
    """Register the search_documents tool with the FastMCP app"""
    
    @app.tool()
    async def search_documents(query: str) -> dict:
        """
        Search documents by keyword or phrase in title, author, content, or category.
        
        Args:
            query: Search query string
        
        Returns:
            Dictionary with list of matching documents
        """
        try:
            # Validate input
            if not query or not query.strip():
                return {
                    "success": False,
                    "error": "Empty query provided",
                    "message": "Please provide a search query"
                }
            
            # Perform search
            matching_documents = document_service.search_documents(query.strip())
            
            # Format results
            results = []
            for doc_summary in matching_documents:
                results.append({
                    "document_id": doc_summary.document_id,
                    "title": doc_summary.title,
                    "author": doc_summary.author,
                    "category": doc_summary.category,
                    "matched": doc_summary.matched
                })
            
            return {
                "success": True,
                "query": query.strip(),
                "results": results,
                "count": len(results),
                "message": f"Found {len(results)} documents matching '{query}'"
            }
            
        except Exception as e:
            logger.error(f"Error in search_documents: {e}")
            return {
                "success": False,
                "error": "Search failed",
                "message": "Failed to search documents due to internal error"
            }
