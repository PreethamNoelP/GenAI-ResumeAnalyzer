import os
import tempfile
from pdfminer.high_level import extract_text
from docx import Document
from typing import Optional
import config

class FileProcessor:
    """Handles file processing for different document formats"""
    
    @staticmethod
    def validate_file(file) -> tuple[bool, str]:
        """Validate uploaded file format and size"""
        if file is None:
            return False, "No file provided"
        
        # Check file format
        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension not in config.SUPPORTED_FORMATS:
            return False, config.ERROR_MESSAGES["unsupported_format"]
        
        # Check file size (convert to MB)
        file_size_mb = file.size / (1024 * 1024)
        if file_size_mb > config.MAX_FILE_SIZE_MB:
            return False, config.ERROR_MESSAGES["file_too_large"]
        
        return True, "File is valid"
    
    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        """Extract text from PDF or DOCX file"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return extract_text(file_path)
            elif file_extension == '.docx':
                doc = Document(file_path)
                return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        except Exception as e:
            raise Exception(f"Error extracting text from file: {str(e)}")
    
    @staticmethod
    def save_uploaded_file(uploaded_file) -> str:
        """Save uploaded file to temporary location and return path"""
        try:
            # Create temp directory if it doesn't exist
            os.makedirs(config.TEMP_DIR, exist_ok=True)
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=os.path.splitext(uploaded_file.name)[1],
                dir=config.TEMP_DIR
            )
            
            # Write uploaded file content
            temp_file.write(uploaded_file.getbuffer())
            temp_file.close()
            
            return temp_file.name
        except Exception as e:
            raise Exception(f"Error saving uploaded file: {str(e)}")
    
    @staticmethod
    def cleanup_temp_file(file_path: str):
        """Remove temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not remove temporary file {file_path}: {str(e)}")
    
    @staticmethod
    def get_file_info(file) -> dict:
        """Get basic information about the uploaded file"""
        return {
            "name": file.name,
            "size_mb": round(file.size / (1024 * 1024), 2),
            "type": os.path.splitext(file.name)[1].lower()
        } 