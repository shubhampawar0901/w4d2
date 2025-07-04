#!/usr/bin/env python3
"""
Setup script for Document Analyzer MCP Server
Installs dependencies and downloads required models
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Document Analyzer MCP Server...")
    
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Download spaCy English model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model"):
        print("Warning: spaCy model download failed. The server will use fallback methods.")
    
    # Verify .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please create a .env file with your Hugging Face API key:")
        print("HUGGING_FACE_API_KEY=your_token_here")
        sys.exit(1)
    
    print("\n✅ Setup completed successfully!")
    print("\n🎯 Next steps:")
    print("1. Verify your .env file contains the correct Hugging Face API key")
    print("2. Run the server: python main.py")
    print("3. Test the MCP tools with your favorite MCP client")
    
    print("\n📚 Available MCP Tools:")
    print("- add_document: Store new documents")
    print("- analyze_document: Complete text analysis")
    print("- get_sentiment: Sentiment analysis")
    print("- extract_keywords: Keyword extraction")
    print("- search_documents: Document search")

if __name__ == "__main__":
    main()
