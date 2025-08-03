import streamlit as st
import asyncio
import nest_asyncio
from pages.home import render_home
from pages.resume_analyzer import render_resume_analyzer
from pages.chatbot import render_chatbot
import config

# Apply nest_asyncio for async support in Streamlit
nest_asyncio.apply()

def main():
    """Main application entry point"""
    
    # Configure page settings
    st.set_page_config(
        page_title=config.PAGE_TITLE,
        layout=config.LAYOUT,
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton > button {
        border-radius: 10px;
        border: 2px solid #667eea;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        border-color: #764ba2;
    }
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div class="main-header">
            <h2>AI Resume Analyzer</h2>
            <p>Batch Processing & Analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("### Navigation")
        page = st.radio(
            "Choose a page:",
            ["Home", "Resume Analyzer", "Chatbot"],
            index=0
        )
        
        # System status
        st.markdown("### System Status")
        
        # Check API key
        if config.GEMINI_API_KEY:
            st.success("API Key Configured")
        else:
            st.error("API Key Missing")
            st.info("Please set GEMINI_API_KEY in your .env file")
        
        # Check directories
        import os
        if os.path.exists(config.OUTPUT_DIR):
            st.success("Output Directory Ready")
        else:
            st.warning("Output Directory Missing")
        
        if os.path.exists(config.TEMP_DIR):
            st.success("Temp Directory Ready")
        else:
            st.warning("Temp Directory Missing")
        
        # Configuration info
        st.markdown("### Configuration")
        st.markdown(f"""
        - **Batch Size**: {config.BATCH_SIZE}
        - **Max Concurrent**: {config.MAX_CONCURRENT_REQUESTS}
        - **Rate Limit**: {config.RATE_LIMIT_DELAY}s
        - **File Size Limit**: {config.MAX_FILE_SIZE_MB}MB
        """)
        
        # Quick actions
        st.markdown("### Quick Actions")
        
        if st.button("Cleanup Temp Files", use_container_width=True):
            cleanup_temp_files()
        
        if st.button("View Output Directory", use_container_width=True):
            show_output_directory()
    
    # Main content area
    try:
        if page == "Home":
            render_home()
        elif page == "Resume Analyzer":
            render_resume_analyzer()
        elif page == "Chatbot":
            render_chatbot()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your configuration and try again.")

def cleanup_temp_files():
    """Clean up temporary files"""
    import os
    import shutil
    
    try:
        if os.path.exists(config.TEMP_DIR):
            shutil.rmtree(config.TEMP_DIR)
            os.makedirs(config.TEMP_DIR, exist_ok=True)
            st.success("Temporary files cleaned up successfully!")
        else:
            st.info("No temporary directory found.")
    except Exception as e:
        st.error(f"Failed to cleanup temp files: {str(e)}")

def show_output_directory():
    """Show contents of output directory"""
    import os
    
    try:
        if os.path.exists(config.OUTPUT_DIR):
            files = os.listdir(config.OUTPUT_DIR)
            if files:
                st.info(f"Output directory contains {len(files)} files:")
                for file in files:
                    st.write(f"  - {file}")
            else:
                st.info("Output directory is empty.")
        else:
            st.warning("Output directory does not exist.")
    except Exception as e:
        st.error(f"Failed to read output directory: {str(e)}")

if __name__ == "__main__":
    main() 