# AI Resume Analyzer - Batch Processing System

A powerful AI-powered resume analysis tool designed for processing large volumes of resumes (100+ files) with advanced batch processing capabilities, built with Streamlit and Google Gemini AI.

## 🚀 Features

### Core Capabilities
- **Batch Processing**: Handle 100+ resumes simultaneously
- **AI-Powered Analysis**: Extract detailed information using Google Gemini AI
- **Multiple Formats**: Support for PDF and DOCX files
- **Progress Tracking**: Real-time progress monitoring
- **Export Options**: Excel and JSON output formats
- **Interactive Chatbot**: Ask questions about analyzed data
- **Rate Limiting**: Optimized API usage with configurable limits

### Technical Features
- **Asynchronous Processing**: Non-blocking batch operations
- **Configurable Settings**: Adjustable batch sizes and processing parameters
- **Error Handling**: Comprehensive error management and recovery
- **Memory Optimization**: Efficient resource management
- **Temporary File Management**: Automatic cleanup of processing files

## 📊 Analysis Capabilities

The system extracts and analyzes:
- **Personal Information**: Name, contact details, location
- **Education**: University, course, discipline, CGPA/percentage
- **Skills**: Technical skills, programming languages, tools
- **Experience Scores**: AI/ML experience, Gen AI experience, overall experience
- **Supporting Information**: Certifications, internships, projects, achievements

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-resume-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

4. **Install spaCy model** (required for text processing)
   ```bash
   python -m spacy download en_core_web_sm
   ```

## 🚀 Usage

### Running the Application

1. **Start the application**
   ```bash
   streamlit run main.py
   ```

2. **Access the web interface**
   - Open your browser and go to `http://localhost:8501`
   - Navigate through the different pages using the sidebar

### Using the Resume Analyzer

1. **Upload Files**
   - Go to the "Resume Analyzer" page
   - Upload multiple PDF or DOCX files
   - View file information and validation

2. **Configure Settings**
   - Adjust batch size (1-20 files)
   - Set maximum concurrent requests (1-10)
   - Configure rate limit delay (0.5-5 seconds)

3. **Start Analysis**
   - Click "Start Analysis" to begin processing
   - Monitor progress in real-time
   - View results and download reports

4. **Export Results**
   - Download Excel reports with formatted data
   - Export JSON files with detailed analysis
   - View summary statistics and metrics

### Using the Chatbot

1. **Load Analysis Context**
   - Upload previous JSON analysis results
   - Provide context for chatbot queries

2. **Ask Questions**
   - Use natural language to query analyzed data
   - Get insights about candidates and skills
   - Explore patterns and trends

## 📁 Project Structure

```
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
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

## ⚙️ Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key

### Configurable Parameters
- **Batch Size**: Number of files processed simultaneously (1-20)
- **Max Concurrent Requests**: Maximum API calls at once (1-10)
- **Rate Limit Delay**: Delay between API calls (0.5-5 seconds)
- **File Size Limit**: Maximum file size in MB (default: 10MB)
- **Supported Formats**: PDF and DOCX files

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Max Batch Size | 20 files |
| Max Concurrent Requests | 10 |
| File Size Limit | 10 MB |
| Supported Formats | PDF, DOCX |
| Processing Speed | ~2-5 seconds per resume |

## 🔧 Advanced Features

### Batch Processing
- Configurable batch sizes for optimal performance
- Asynchronous processing with progress tracking
- Error handling and recovery mechanisms
- Memory-efficient file processing

### Output Generation
- **Excel Reports**: Formatted spreadsheets with auto-adjusted columns
- **JSON Reports**: Detailed structured data with metadata
- **Summary Statistics**: Success rates, average scores, error analysis

### Error Handling
- File validation and format checking
- API error recovery and retry logic
- Temporary file cleanup
- Comprehensive error reporting

## 🤖 AI Analysis Features

### Extracted Information
- **Personal Details**: Name, email, phone, location
- **Education**: University, course, year, CGPA
- **Skills**: Technical skills, programming languages, tools
- **Experience**: AI/ML scores, Gen AI experience, overall rating
- **Projects**: Certifications, internships, achievements

### Scoring System
- **AI/ML Experience**: 1-10 scale based on relevant experience
- **Gen AI Experience**: 1-10 scale for generative AI knowledge
- **Overall Experience**: 1-10 scale for general technical experience
- **Confidence Score**: Analysis quality assessment

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `GEMINI_API_KEY` is set in `.env` file
   - Verify API key is valid and has sufficient quota

2. **File Upload Issues**
   - Check file format (PDF/DOCX only)
   - Ensure file size is under 10MB
   - Verify file is not corrupted

3. **Processing Errors**
   - Check internet connection
   - Verify API rate limits
   - Monitor system resources

4. **Memory Issues**
   - Reduce batch size
   - Clean up temporary files
   - Restart application if needed

### Performance Optimization

1. **For Large Batches (100+ files)**
   - Use smaller batch sizes (5-10 files)
   - Increase rate limit delay (2-3 seconds)
   - Monitor system resources

2. **For Faster Processing**
   - Increase batch size (15-20 files)
   - Reduce rate limit delay (0.5-1 second)
   - Ensure stable internet connection

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section
- Review the configuration settings

## 🔄 Version History

- **v2.0.0**: Enhanced batch processing, async operations, improved UI
- **v1.0.0**: Initial release with basic functionality

---

**Built using Streamlit and Google Gemini AI** 
