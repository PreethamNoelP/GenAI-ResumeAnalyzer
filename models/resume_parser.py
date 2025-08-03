import json
import asyncio
import time
from typing import List, Dict, Any
import google.generativeai as genai
from utils.file_processor import FileProcessor
import config

class ResumeParser:
    """Handles AI-powered resume analysis with batch processing capabilities"""
    
    def __init__(self):
        """Initialize the resume parser with Gemini API configuration"""
        if not config.GEMINI_API_KEY:
            raise ValueError(config.ERROR_MESSAGES["no_api_key"])
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
        self.file_processor = FileProcessor()
    
    def create_analysis_prompt(self, text: str) -> str:
        """Create the analysis prompt for resume text"""
        return f"""
        Analyze the following resume and extract the following information in JSON format:
        
        {{
            "name": "Full name of the person",
            "contact_details": {{
                "email": "Email address",
                "phone": "Phone number",
                "location": "City, State/Country"
            }},
            "education": {{
                "university": "University/Institution name",
                "year_of_study": "Current year or graduation year",
                "course": "Degree program name",
                "discipline": "Field of study",
                "cgpa_percentage": "CGPA or percentage if available"
            }},
            "skills": {{
                "technical_skills": ["List of technical skills"],
                "soft_skills": ["List of soft skills"],
                "programming_languages": ["List of programming languages"],
                "tools_technologies": ["List of tools and technologies"]
            }},
            "experience_scores": {{
                "ai_ml_experience": "Score from 1-10 based on AI/ML experience",
                "gen_ai_experience": "Score from 1-10 based on Gen AI experience",
                "overall_experience": "Score from 1-10 based on overall experience"
            }},
            "supporting_information": {{
                "certifications": ["List of relevant certifications"],
                "internships": ["List of internships"],
                "projects": ["List of relevant projects"],
                "achievements": ["List of achievements"]
            }},
            "analysis_metadata": {{
                "processing_timestamp": "Current timestamp",
                "file_name": "Original file name",
                "confidence_score": "Confidence in analysis (1-10)"
            }}
        }}
        
        Resume text:
        {text}
        
        Please ensure the response is valid JSON format only.
        """
    
    async def analyze_single_resume(self, file_path: str, file_name: str) -> Dict[str, Any]:
        """Analyze a single resume asynchronously"""
        try:
            # Extract text from file
            text = self.file_processor.extract_text_from_file(file_path)
            
            # Create analysis prompt
            prompt = self.create_analysis_prompt(text)
            
            # Call Gemini API
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            analysis_result = json.loads(response.text.strip())
            
            # Add metadata
            analysis_result["analysis_metadata"]["file_name"] = file_name
            analysis_result["analysis_metadata"]["processing_timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            return analysis_result
            
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse AI response as JSON: {str(e)}",
                "file_name": file_name,
                "raw_response": response.text if 'response' in locals() else "No response"
            }
        except Exception as e:
            return {
                "error": f"Error analyzing resume: {str(e)}",
                "file_name": file_name
            }
    
    async def process_batch(self, files: List, progress_callback=None) -> List[Dict[str, Any]]:
        """Process a batch of resumes with rate limiting and progress tracking"""
        results = []
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_REQUESTS)
        
        async def process_file(file):
            async with semaphore:
                # Validate file
                is_valid, error_msg = self.file_processor.validate_file(file)
                if not is_valid:
                    return {"error": error_msg, "file_name": file.name}
                
                # Save file temporarily
                temp_file_path = self.file_processor.save_uploaded_file(file)
                
                try:
                    # Analyze resume
                    result = await self.analyze_single_resume(temp_file_path, file.name)
                    
                    # Add file info
                    result["file_info"] = self.file_processor.get_file_info(file)
                    
                    return result
                    
                finally:
                    # Cleanup temporary file
                    self.file_processor.cleanup_temp_file(temp_file_path)
        
        # Process files in batches
        for i in range(0, len(files), config.BATCH_SIZE):
            batch = files[i:i + config.BATCH_SIZE]
            
            # Create tasks for current batch
            tasks = [process_file(file) for file in batch]
            
            # Execute batch with progress tracking
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle exceptions and add to results
            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    results.append({
                        "error": f"Processing error: {str(result)}",
                        "file_name": batch[j].name
                    })
                else:
                    results.append(result)
            
            # Update progress
            if progress_callback:
                progress = min((i + len(batch)) / len(files) * 100, 100)
                progress_callback(progress)
            
            # Rate limiting delay between batches
            if i + config.BATCH_SIZE < len(files):
                await asyncio.sleep(config.RATE_LIMIT_DELAY)
        
        return results
    
    def analyze_resumes_sync(self, files: List) -> List[Dict[str, Any]]:
        """Synchronous wrapper for batch processing"""
        return asyncio.run(self.process_batch(files)) 