import streamlit as st
import google.generativeai as genai
import config

def render_chatbot():
    """Render the chatbot page for resume analysis queries"""
    
    st.title("Resume Analysis Chatbot")
    st.markdown("Ask questions about the analyzed resumes and get AI-powered insights")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Initialize Gemini model
    if 'chat_model' not in st.session_state:
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            st.session_state.chat_model = genai.GenerativeModel(config.MODEL_NAME)
        except Exception as e:
            st.error(f"Failed to initialize chatbot: {str(e)}")
            st.stop()
    
    # Display chat interface
    st.header("Chat Interface")
    
    # Chat input
    user_question = st.text_area(
        "Ask a question about the analyzed resumes:",
        placeholder="e.g., Who has the highest AI/ML experience score? Which candidates have Python skills?",
        height=100
    )
    
    # Analysis context (if available)
    analysis_context = ""
    if 'analysis_results' in st.session_state and st.session_state.analysis_results:
        analysis_context = f"""
        Based on the following resume analysis results, answer the user's question:
        
        {st.session_state.analysis_results}
        """
    
    # Chat controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("Ask AI", type="primary", use_container_width=True):
            if not user_question.strip():
                st.error("Please enter a question.")
            else:
                process_chat_question(user_question, analysis_context)
    
    with col2:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Display chat history
    if st.session_state.chat_history:
        st.header("Chat History")
        
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.expander(f"Q{i+1}: {question[:50]}...", expanded=False):
                st.markdown(f"**Question:** {question}")
                st.markdown(f"**Answer:** {answer}")
    
    # Sample questions
    st.header("Sample Questions")
    
    sample_questions = [
        "Which candidates have the highest AI/ML experience scores?",
        "Who has experience with Python and machine learning?",
        "Which universities are most represented in the resumes?",
        "Who has certifications in AI or data science?",
        "Which candidates have internship experience?",
        "What are the most common technical skills among the candidates?",
        "Who has the highest overall experience score?",
        "Which candidates have projects related to AI or ML?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(sample_questions):
        with cols[i % 2]:
            if st.button(question, key=f"sample_{i}", use_container_width=True):
                process_chat_question(question, analysis_context)

def process_chat_question(question: str, context: str):
    """Process a chat question and generate response"""
    
    try:
        # Create prompt with context
        if context:
            prompt = f"""
            {context}
            
            User Question: {question}
            
            Please provide a detailed and helpful answer based on the resume analysis data.
            If the data doesn't contain relevant information, please mention that.
            """
        else:
            prompt = f"""
            User Question: {question}
            
            Note: No resume analysis data is currently available. 
            Please provide a general response about what kind of insights could be obtained from resume analysis.
            """
        
        # Generate response
        with st.spinner("Thinking..."):
            response = st.session_state.chat_model.generate_content(prompt)
            answer = response.text
        
        # Add to chat history
        st.session_state.chat_history.append((question, answer))
        
        # Display response
        st.success("Response generated!")
        st.markdown(f"**Answer:** {answer}")
        
    except Exception as e:
        st.error(f"Failed to generate response: {str(e)}")

def render_analysis_context_upload():
    """Render section for uploading analysis results for chatbot context"""
    
    st.header("Load Analysis Context")
    st.markdown("Upload previous analysis results to provide context for the chatbot")
    
    uploaded_file = st.file_uploader(
        "Upload JSON analysis results",
        type=["json"],
        help="Upload a JSON file from previous resume analysis"
    )
    
    if uploaded_file and st.button("Load Context"):
        try:
            import json
            analysis_data = json.load(uploaded_file)
            st.session_state.analysis_results = json.dumps(analysis_data, indent=2)
            st.success("Analysis context loaded successfully!")
        except Exception as e:
            st.error(f"Failed to load analysis context: {str(e)}")
    
    # Show current context status
    if 'analysis_results' in st.session_state:
        st.info("Analysis context is loaded and available for chatbot queries")
        with st.expander("View loaded context"):
            st.json(st.session_state.analysis_results)
    else:
        st.warning("No analysis context loaded. Chatbot will provide general responses.") 