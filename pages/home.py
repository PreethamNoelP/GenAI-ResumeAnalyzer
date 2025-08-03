import streamlit as st
import config

def render_home():
    """Render the home page with project overview"""
    
    st.title("Welcome to AI Resume Analyzer")
    st.markdown("### Advanced Batch Processing for Resume Analysis with AI")
    
    # Project overview
    st.header("Project Overview")
    
    st.markdown("""
    This AI-powered resume analyzer provides comprehensive batch processing capabilities for analyzing 
    large volumes of resumes (100+ files) with advanced features:
    
    **Key Features:**
    - **Batch Processing**: Handle 100+ resumes simultaneously
    - **AI-Powered Analysis**: Extract detailed information using Google Gemini AI
    - **Multiple Formats**: Support for PDF and DOCX files
    - **Progress Tracking**: Real-time progress monitoring
    - **Export Options**: Excel and JSON output formats
    - **Interactive Chatbot**: Ask questions about analyzed data
    - **Rate Limiting**: Optimized API usage with configurable limits
    """)
    
    # Technical capabilities
    st.header("Technical Capabilities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Analysis Features:**
        - Name and contact details extraction
        - Educational background analysis
        - Skills and experience scoring
        - AI/ML experience evaluation
        - Project and certification tracking
        - Confidence scoring for analysis quality
        """)
    
    with col2:
        st.markdown("""
        **Processing Features:**
        - Asynchronous batch processing
        - Configurable batch sizes (1-20 files)
        - Concurrent API request management
        - Error handling and recovery
        - Temporary file management
        - Memory optimization
        """)
    
    # Performance metrics
    st.header("Performance Metrics")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric("Max Batch Size", "20 files")
    
    with metrics_col2:
        st.metric("Max Concurrent", "10 requests")
    
    with metrics_col3:
        st.metric("File Size Limit", "10 MB")
    
    with metrics_col4:
        st.metric("Supported Formats", "PDF, DOCX")
    
    # Getting started
    st.header("Getting Started")
    
    st.markdown("""
    1. **Navigate to Resume Analyzer** - Upload your resume files
    2. **Configure Settings** - Adjust batch size and processing parameters
    3. **Start Analysis** - Begin batch processing with progress tracking
    4. **Review Results** - View detailed analysis and download reports
    5. **Use Chatbot** - Ask questions about the analyzed data
    """)
    
    # Configuration requirements
    st.header("Configuration")
    
    with st.expander("Environment Setup"):
        st.markdown("""
        **Required Environment Variables:**
        ```
        GEMINI_API_KEY=your_google_gemini_api_key
        ```
        
        **Installation:**
        ```bash
        pip install -r requirements.txt
        ```
        
        **Running the Application:**
        ```bash
        streamlit run main.py
        ```
        """)
    
    # File structure
    st.header("Project Structure")
    
    st.markdown("""
    ```
    ├── main.py                 # Main application entry point
    ├── config.py              # Configuration settings
    ├── requirements.txt       # Python dependencies
    ├── models/
    │   ├── resume_parser.py   # AI analysis logic
    │   └── __init__.py
    ├── utils/
    │   ├── file_processor.py  # File handling utilities
    │   ├── output_handler.py  # Output generation
    │   └── __init__.py
    ├── pages/
    │   ├── home.py           # Home page
    │   ├── resume_analyzer.py # Main analysis page
    │   ├── chatbot.py        # Chatbot interface
    │   └── __init__.py
    ├── output/               # Generated reports
    └── temp_files/           # Temporary processing files
    ```
    """)
    
    # Features comparison
    st.header("Feature Comparison")
    
    comparison_data = {
        "Feature": [
            "Batch Processing",
            "Progress Tracking", 
            "Error Handling",
            "Export Options",
            "Rate Limiting",
            "Memory Management",
            "Async Processing",
            "Configurable Settings"
        ],
        "Original": [
            "No",
            "No",
            "Basic",
            "Limited",
            "No",
            "Poor",
            "No",
            "No"
        ],
        "Enhanced": [
            "Yes (100+ files)",
            "Yes",
            "Comprehensive",
            "Excel & JSON",
            "Yes",
            "Optimized",
            "Yes",
            "Yes"
        ]
    }
    
    import pandas as pd
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with Streamlit and Google Gemini AI</p>
        <p>Optimized for large-scale resume analysis and batch processing</p>
    </div>
    """, unsafe_allow_html=True) 