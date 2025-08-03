import os
import json
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import config

class OutputHandler:
    """Handles output generation and file management for resume analysis results"""
    
    def __init__(self):
        """Initialize output handler with output directory"""
        self.output_dir = config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
    
    def flatten_resume_data(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten nested resume data for Excel export"""
        flattened_data = []
        
        for result in results:
            if "error" in result:
                # Handle error cases
                flattened_data.append({
                    "file_name": result.get("file_name", "Unknown"),
                    "status": "Error",
                    "error_message": result["error"],
                    "name": "",
                    "email": "",
                    "phone": "",
                    "university": "",
                    "course": "",
                    "cgpa_percentage": "",
                    "technical_skills": "",
                    "ai_ml_experience": "",
                    "gen_ai_experience": "",
                    "overall_experience": "",
                    "certifications": "",
                    "projects": "",
                    "processing_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                continue
            
            # Extract basic information
            name = result.get("name", "")
            contact_details = result.get("contact_details", {})
            education = result.get("education", {})
            skills = result.get("skills", {})
            experience_scores = result.get("experience_scores", {})
            supporting_info = result.get("supporting_information", {})
            metadata = result.get("analysis_metadata", {})
            
            # Flatten the data
            flattened_row = {
                "file_name": metadata.get("file_name", ""),
                "status": "Success",
                "error_message": "",
                "name": name,
                "email": contact_details.get("email", ""),
                "phone": contact_details.get("phone", ""),
                "location": contact_details.get("location", ""),
                "university": education.get("university", ""),
                "year_of_study": education.get("year_of_study", ""),
                "course": education.get("course", ""),
                "discipline": education.get("discipline", ""),
                "cgpa_percentage": education.get("cgpa_percentage", ""),
                "technical_skills": ", ".join(skills.get("technical_skills", [])),
                "soft_skills": ", ".join(skills.get("soft_skills", [])),
                "programming_languages": ", ".join(skills.get("programming_languages", [])),
                "tools_technologies": ", ".join(skills.get("tools_technologies", [])),
                "ai_ml_experience": experience_scores.get("ai_ml_experience", ""),
                "gen_ai_experience": experience_scores.get("gen_ai_experience", ""),
                "overall_experience": experience_scores.get("overall_experience", ""),
                "certifications": ", ".join(supporting_info.get("certifications", [])),
                "internships": ", ".join(supporting_info.get("internships", [])),
                "projects": ", ".join(supporting_info.get("projects", [])),
                "achievements": ", ".join(supporting_info.get("achievements", [])),
                "confidence_score": metadata.get("confidence_score", ""),
                "processing_timestamp": metadata.get("processing_timestamp", "")
            }
            
            flattened_data.append(flattened_row)
        
        return flattened_data
    
    def save_to_excel(self, results: List[Dict[str, Any]], filename: str = None) -> str:
        """Save results to Excel file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_analysis_{timestamp}.xlsx"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Flatten data for Excel
        flattened_data = self.flatten_resume_data(results)
        
        # Create DataFrame
        df = pd.DataFrame(flattened_data)
        
        # Save to Excel with formatting
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Resume Analysis', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Resume Analysis']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return filepath
    
    def save_to_json(self, results: List[Dict[str, Any]], filename: str = None) -> str:
        """Save results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_analysis_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Add metadata to results
        output_data = {
            "metadata": {
                "total_resumes": len(results),
                "successful_analyses": len([r for r in results if "error" not in r]),
                "failed_analyses": len([r for r in results if "error" in r]),
                "generated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            "results": results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def generate_summary_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics from analysis results"""
        successful_results = [r for r in results if "error" not in r]
        failed_results = [r for r in results if "error" in r]
        
        stats = {
            "total_files": len(results),
            "successful_analyses": len(successful_results),
            "failed_analyses": len(failed_results),
            "success_rate": len(successful_results) / len(results) * 100 if results else 0
        }
        
        if successful_results:
            # Calculate average experience scores
            ai_scores = []
            gen_ai_scores = []
            overall_scores = []
            
            for result in successful_results:
                experience_scores = result.get("experience_scores", {})
                if experience_scores.get("ai_ml_experience"):
                    try:
                        ai_scores.append(float(experience_scores["ai_ml_experience"]))
                    except:
                        pass
                if experience_scores.get("gen_ai_experience"):
                    try:
                        gen_ai_scores.append(float(experience_scores["gen_ai_experience"]))
                    except:
                        pass
                if experience_scores.get("overall_experience"):
                    try:
                        overall_scores.append(float(experience_scores["overall_experience"]))
                    except:
                        pass
            
            stats.update({
                "avg_ai_ml_experience": sum(ai_scores) / len(ai_scores) if ai_scores else 0,
                "avg_gen_ai_experience": sum(gen_ai_scores) / len(gen_ai_scores) if gen_ai_scores else 0,
                "avg_overall_experience": sum(overall_scores) / len(overall_scores) if overall_scores else 0
            })
        
        return stats
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up old output files"""
        current_time = datetime.now()
        
        for filename in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, filename)
            if os.path.isfile(filepath):
                file_age = current_time - datetime.fromtimestamp(os.path.getctime(filepath))
                if file_age.total_seconds() > max_age_hours * 3600:
                    try:
                        os.remove(filepath)
                    except Exception as e:
                        print(f"Could not remove old file {filepath}: {e}") 