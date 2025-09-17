# AI Baba Admin System - Complete Setup Guide

## 🧿 Overview

The AI Baba Admin System is a comprehensive data collection and processing platform designed for managing spiritual advice content. It features advanced text cleaning, AI-powered categorization, and seamless Supabase database integration.

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Supabase account and project
- At least 4GB RAM (for AI models)
- Internet connection (for downloading AI models)

### 2. Clone and Setup

```bash
cd ai-baba
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env file with your Supabase credentials
```

### 4. Launch the System

```bash
python run_admin.py
```

The admin interface will open in your browser at `http://localhost:8501`

## 🔧 Detailed Setup Instructions

### Step 1: Supabase Configuration

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Note your Project URL and Anon Key

2. **Create Database Table**
   - Go to SQL Editor in your Supabase dashboard
   - Run this SQL to create the required table:

```sql
CREATE TABLE advice_dataset (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    subcategories TEXT,
    information TEXT NOT NULL,
    original_text TEXT,
    confidence_score FLOAT,
    processing_metadata JSONB,
    admin_confirmed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create indexes for better performance
CREATE INDEX idx_advice_category ON advice_dataset (category);
CREATE INDEX idx_advice_confirmed ON advice_dataset (admin_confirmed);
CREATE INDEX idx_advice_created_at ON advice_dataset (created_at);
```

3. **Configure Environment Variables**
   - Edit `.env` file:

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
- `streamlit` - Web interface
- `supabase` - Database integration
- `transformers` - Hugging Face AI models
- `torch` - Deep learning framework
- `sentence-transformers` - Sentence embeddings
- `scikit-learn` - Machine learning utilities
- `pandas` - Data manipulation
- `nltk` - Natural language processing
- `spacy` - Advanced NLP

### Step 3: Download AI Models

The system will automatically download required models on first run:

```bash
# NLTK data (automatic)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# spaCy English model (automatic)
python -m spacy download en_core_web_sm
```

### Step 4: Launch Application

```bash
python run_admin.py
```

## 📋 System Features

### 🧹 Advanced Text Processing
- **Originality Preservation**: Cleans text while maintaining original meaning
- **Multi-language Support**: Detects and processes multiple languages  
- **Encoding Fix**: Handles Unicode and encoding issues
- **Duplicate Detection**: Identifies and prevents duplicate content
- **Spiritual Terms Preservation**: Maintains important spiritual terminology

### 🤖 AI-Powered Classification
- **Zero-shot Classification**: Uses BART model for category assignment
- **Sentence Embeddings**: Semantic similarity using sentence transformers
- **Keyword Matching**: Rule-based classification backup
- **Ensemble Methods**: Combines multiple approaches for better accuracy
- **Multi-label Support**: Assigns multiple subcategories when appropriate

### 💾 Database Management
- **Real-time Storage**: Immediate saving to Supabase
- **Search Functionality**: Full-text search across content
- **Admin Confirmation**: Review process before final storage
- **Export Capabilities**: CSV export for analysis
- **Analytics Dashboard**: Comprehensive statistics and insights

## 📊 Category Structure

The system supports 12 main categories with detailed subcategories:

### Main Categories:
1. **Emotional Support** (6 subcategories)
2. **Motivation & Self-Growth** (7 subcategories)
3. **Failures & Mistakes** (6 subcategories)
4. **Decision Making & Life Choices** (5 subcategories)
5. **Relationships & Social Life** (6 subcategories)
6. **Career & Studies** (6 subcategories)
7. **Health & Lifestyle** (5 subcategories)
8. **Money & Finance** (5 subcategories)
9. **Spiritual / Philosophical** (6 subcategories)
10. **General Curiosity & Learning** (5 subcategories)
11. **Smoking & Drinking Habits** (4 subcategories)
12. **Masturbation & Sexual Health** (4 subcategories)

## 🎯 Usage Workflow

### 1. Text Processing
1. Navigate to "Text Processing" page
2. Paste raw text in the input area
3. Configure processing options
4. Click "Process Text"

### 2. Review Results
- **Cleaned Text Tab**: Compare original vs cleaned text
- **Analysis Tab**: View processing details and statistics
- **Classification Tab**: Review AI-assigned categories
- **Save Tab**: Confirm and store in database

### 3. Database Management
- View recent entries
- Search existing content
- Export data for analysis
- Monitor system statistics

### 4. Analytics
- View data summaries
- Export to CSV
- Monitor processing trends
- Category distribution analysis

## ⚙️ Configuration Options

### Environment Variables (.env)
```env
# Required
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key

# Optional
DEBUG=False
LOG_LEVEL=INFO
MAX_TEXT_LENGTH=50000
DEFAULT_CONFIDENCE_THRESHOLD=0.3
ENABLE_GPU=False
```

### Processing Settings
- **Preserve Formatting**: Maintain original text structure
- **Duplicate Detection**: Check for existing similar content
- **Auto-Categorize**: Enable AI classification
- **Confidence Threshold**: Minimum confidence for auto-assignment

## 🔍 Troubleshooting

### Common Issues

**1. Database Connection Failed**
- Verify Supabase URL and key in `.env`
- Check internet connection
- Ensure table exists in database

**2. AI Models Not Loading**
- Check internet connection for model download
- Increase system RAM if models fail to load
- Try running without GPU acceleration

**3. Import Errors**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ required)
- Verify virtual environment activation

**4. Streamlit Errors**
- Clear browser cache
- Try different browser
- Check port 8501 availability

### Performance Optimization

**For Better Speed:**
- Enable GPU if available (`ENABLE_GPU=True`)
- Increase system RAM
- Use SSD storage for models

**For Lower Resource Usage:**
- Set `ENABLE_GPU=False`
- Process smaller text batches
- Disable zero-shot classifier in code

## 📁 Project Structure

```
ai-baba/
├── admin_system/           # Admin interface modules
│   ├── admin_interface.py  # Main Streamlit app
│   └── database.py         # Database operations
├── config/                 # Configuration files
│   └── supabase_config.py  # Supabase setup
├── models/                 # AI models
│   └── text_classifier.py  # Classification system
├── utils/                  # Utility modules
│   ├── categories.py       # Category definitions
│   └── text_processor.py   # Text processing
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── run_admin.py           # Application launcher
└── SETUP_GUIDE.md         # This file
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` file to version control
2. **Database Access**: Use Row Level Security (RLS) in Supabase
3. **API Keys**: Rotate keys periodically
4. **User Authentication**: Implement proper auth for production

## 📈 Scaling Considerations

For larger deployments:

1. **Database**: Consider read replicas for analytics
2. **Processing**: Implement background job queues
3. **Caching**: Add Redis for model caching
4. **Monitoring**: Set up logging and metrics

## 🆘 Support

For issues and questions:

1. Check this setup guide thoroughly
2. Review error messages in console
3. Test database connection in Settings page
4. Verify all dependencies are installed

## 🚀 Advanced Features

### Batch Processing
- Process multiple texts at once
- Background processing capabilities
- Progress tracking and reporting

### Custom Categories
- Modify category structure in `utils/categories.py`
- Add custom keywords and prompts
- Update database schema if needed

### API Integration
- Extend for REST API endpoints
- Webhook support for real-time processing
- Integration with external systems

---

🧿 **AI Baba Admin System** - Transforming spiritual wisdom through advanced AI technology
