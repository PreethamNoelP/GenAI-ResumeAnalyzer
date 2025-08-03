import streamlit as st
import asyncio
from typing import List
import pandas as pd
from models.resume_parser import ResumeParser
from utils.output_handler import OutputHandler
import config

def render_resume_analyzer():
    """Render the resume analyzer page with batch processing capabilities"""
    
    st.title("Resume Analyzer")
    st.markdown("Upload multiple resumes for batch analysis with AI-powered insights")
    
    # Initialize components
    if 'resume_parser' not in st.session_state:
        try:
            st.session_state.resume_parser = ResumeParser()
        except ValueError as e:
            st.error(str(e))
            st.stop()
    
    if 'output_handler' not in st.session_state:
        st.session_state.output_handler = OutputHandler()
    
    # File upload section
    st.header("Upload Resumes")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_files = st.file_uploader(
            "Choose resume files",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="Upload multiple PDF or DOCX files for batch processing"
        )
    
    with col2:
        st.metric("Files Selected", len(uploaded_files) if uploaded_files else 0)
    
    # Display file information
    if uploaded_files:
        st.subheader("File Information")
        
        file_info = []
        for file in uploaded_files:
            file_info.append({
                "Name": file.name,
                "Size (MB)": round(file.size / (1024 * 1024), 2),
                "Type": file.type
            })
        
        df_files = pd.DataFrame(file_info)
        st.dataframe(df_files, use_container_width=True)
    
    # Analysis controls
    if uploaded_files and len(uploaded_files) > 0:
        st.header("Analysis Settings")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            batch_size = st.slider(
                "Batch Size",
                min_value=1,
                max_value=20,
                value=config.BATCH_SIZE,
                help="Number of resumes to process simultaneously"
            )
        
        with col2:
            max_concurrent = st.slider(
                "Max Concurrent Requests",
                min_value=1,
                max_value=10,
                value=config.MAX_CONCURRENT_REQUESTS,
                help="Maximum concurrent API calls"
            )
        
        with col3:
            rate_limit = st.slider(
                "Rate Limit Delay (seconds)",
                min_value=0.5,
                max_value=5.0,
                value=config.RATE_LIMIT_DELAY,
                step=0.5,
                help="Delay between API calls"
            )
        
        # Start analysis button
        if st.button("Start Analysis", type="primary", use_container_width=True):
            asyncio.run(run_batch_analysis(uploaded_files, batch_size, max_concurrent, rate_limit))

async def run_batch_analysis(files: List, batch_size: int, max_concurrent: int, rate_limit: float):
    """Run batch analysis with progress tracking"""
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Create results container
    results_container = st.container()
    
    try:
        # Update configuration for this run
        config.BATCH_SIZE = batch_size
        config.MAX_CONCURRENT_REQUESTS = max_concurrent
        config.RATE_LIMIT_DELAY = rate_limit
        
        # Initialize parser
        parser = ResumeParser()
        output_handler = OutputHandler()
        
        # Progress callback
        def update_progress(progress):
            progress_bar.progress(progress / 100)
            status_text.text(f"Processing... {progress:.1f}%")
        
        # Run analysis
        status_text.text("Starting analysis...")
        results = await parser.process_batch(files, update_progress)
        
        # Display results
        with results_container:
            display_analysis_results(results, output_handler)
            
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()

def display_analysis_results(results: List, output_handler: OutputHandler):
    """Display analysis results with summary and download options"""
    
    st.header("Analysis Results")
    
    # Generate summary statistics
    stats = output_handler.generate_summary_stats(results)
    
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Files", stats["total_files"])
    
    with col2:
        st.metric("Successful", stats["successful_analyses"])
    
    with col3:
        st.metric("Failed", stats["failed_analyses"])
    
    with col4:
        st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
    
    # Display experience scores if available
    if stats.get("avg_ai_ml_experience") > 0:
        st.subheader("Experience Scores (Average)")
        
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        
        with exp_col1:
            st.metric("AI/ML Experience", f"{stats['avg_ai_ml_experience']:.1f}/10")
        
        with exp_col2:
            st.metric("Gen AI Experience", f"{stats['avg_gen_ai_experience']:.1f}/10")
        
        with exp_col3:
            st.metric("Overall Experience", f"{stats['avg_overall_experience']:.1f}/10")
    
    # Display detailed results
    st.subheader("Detailed Results")
    
    # Separate successful and failed results
    successful_results = [r for r in results if "error" not in r]
    failed_results = [r for r in results if "error" in r]
    
    # Show successful results
    if successful_results:
        st.success(f"Successfully analyzed {len(successful_results)} resumes")
        
        # Create a summary table
        summary_data = []
        for result in successful_results:
            summary_data.append({
                "Name": result.get("name", "N/A"),
                "University": result.get("education", {}).get("university", "N/A"),
                "Course": result.get("education", {}).get("course", "N/A"),
                "AI/ML Score": result.get("experience_scores", {}).get("ai_ml_experience", "N/A"),
                "Gen AI Score": result.get("experience_scores", {}).get("gen_ai_experience", "N/A"),
                "File": result.get("analysis_metadata", {}).get("file_name", "N/A")
            })
        
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True)
    
    # Show failed results
    if failed_results:
        st.error(f"Failed to analyze {len(failed_results)} resumes")
        
        error_data = []
        for result in failed_results:
            error_data.append({
                "File": result.get("file_name", "Unknown"),
                "Error": result.get("error", "Unknown error")
            })
        
        df_errors = pd.DataFrame(error_data)
        st.dataframe(df_errors, use_container_width=True)
    
    # Download options
    st.header("Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Download Excel Report", use_container_width=True):
            try:
                excel_path = output_handler.save_to_excel(results)
                with open(excel_path, "rb") as f:
                    st.download_button(
                        label="Click to Download Excel",
                        data=f.read(),
                        file_name=f"resume_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"Failed to generate Excel report: {str(e)}")
    
    with col2:
        if st.button("Download JSON Report", use_container_width=True):
            try:
                json_path = output_handler.save_to_json(results)
                with open(json_path, "rb") as f:
                    st.download_button(
                        label="Click to Download JSON",
                        data=f.read(),
                        file_name=f"resume_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            except Exception as e:
                st.error(f"Failed to generate JSON report: {str(e)}")
    
    # Show raw results in expandable section
    with st.expander("View Raw Analysis Data"):
        st.json(results) 