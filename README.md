# 🧿 AI Baba - Integrated Wisdom & Admin System

A comprehensive spiritual guidance platform with advanced data collection and AI-powered categorization capabilities. AI Baba combines a user-friendly spiritual advice chatbot with a powerful admin system for managing wisdom content from spiritual masters like Osho, Buddha, and Sadhguru.

## 🚀 System Features

### 👤 User Interface
- **Spiritual Guidance Chatbot**: Interactive AI companion for life's challenges
- **Personalized Advice**: Contextual responses based on mood and situation
- **Conversation History**: Track your spiritual journey
- **Clean, Intuitive Design**: Easy-to-use interface for all users

### ⚙️ Admin Interface (Comprehensive Management System)

#### 📊 **Dashboard**
- Real-time system status monitoring
- Database connection health checks
- AI model status indicators
- Quick statistics overview

#### 📝 **Advanced Data Collection**
- **Text Processing**: Advanced cleaning while preserving originality
- **AI Categorization**: Zero-shot classification, embeddings, keyword matching
- **12 Main Categories**: Emotional Support, Motivation, Relationships, etc.
- **65+ Subcategories**: Detailed classification system
- **Admin Review Process**: Human confirmation before storage

#### 💾 **Database Management**
- Complete Supabase integration
- Real-time data storage and retrieval
- Advanced search functionality
- Entry management (view, edit, delete)

#### 📈 **Analytics & Insights**
- Comprehensive data analytics
- Category distribution visualization
- Data export capabilities (CSV)
- Performance metrics tracking

#### 🔧 **System Configuration**
- AI model management
- Database connection testing
- Category structure management
- Processing parameter tuning

#### 📋 **System Monitoring**
- Real-time logging system
- System health monitoring
- Error tracking and reporting
- Performance metrics

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- Supabase account and project
- At least 4GB RAM (for AI models)
- Internet connection (for downloading AI models)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
copy .env.example .env

# Edit .env with your Supabase credentials:
# SUPABASE_URL=your_project_url
# SUPABASE_ANON_KEY=your_anon_key
```

### 3. Setup Database (Supabase)
Create table with this SQL:
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

-- Indexes for performance
CREATE INDEX idx_advice_category ON advice_dataset (category);
CREATE INDEX idx_advice_confirmed ON advice_dataset (admin_confirmed);
CREATE INDEX idx_advice_created_at ON advice_dataset (created_at);
```

### 4. Launch System
```bash
# Method 1: Use the enhanced launcher (recommended)
python launch_ai_baba.py

# Method 2: Direct Streamlit launch
streamlit run app.py
```

### 5. Access the System
- **URL**: http://localhost:8501
- **User Interface**: Select "User Interface" in sidebar
- **Admin Interface**: Select "Admin Interface" → Enter key: `admin123`

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Models**: Hugging Face Transformers, Sentence Transformers
- **NLP**: NLTK, spaCy, scikit-learn
- **Database**: Supabase (PostgreSQL)
- **ML Framework**: PyTorch
- **Data Processing**: pandas, numpy

## 🏗️ Project Structure

```
ai-baba/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── venv/              # Virtual environment (auto-generated)
└── .gitignore         # Git ignore file (to be created)
```

## 🎯 Future Enhancements

This is the initial setup with blank interfaces. Future features to be implemented:

### User Interface Enhancements
- [ ] AI chatbot integration (OpenAI, Anthropic, or local models)
- [ ] Conversation persistence (database storage)
- [ ] User authentication and profiles
- [ ] Multiple conversation threads
- [ ] Export conversation history
- [ ] Voice input/output capabilities

### Admin Interface Enhancements
- [ ] Real-time analytics and reporting
- [ ] User management system
- [ ] Conversation moderation tools
- [ ] System performance monitoring
- [ ] Configuration file management
- [ ] Backup and restore functionality

### Technical Improvements
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Session state management
- [ ] Error handling and logging
- [ ] Unit and integration tests
- [ ] Docker containerization
- [ ] API endpoints for external integration

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **UI Components**: Streamlit widgets and components
- **Package Management**: pip + requirements.txt

## 📝 Development Notes

- The application uses Streamlit's built-in session state for temporary data storage
- Admin authentication is currently a simple password check (placeholder)
- All chat functionality is currently placeholder - ready for AI integration
- The design follows a mystical/ancient wisdom theme with appropriate emojis and styling

## 🤝 Contributing

This project is in early development. Contributions and suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request



## 🔮 About AI Baba

AI Baba draws inspiration from the wise storytellers and advisors of ancient times, combining traditional wisdom with modern AI capabilities to provide thoughtful guidance for life's challenges. The conversational style aims to be warm, insightful, and encouraging while maintaining a mystical and wise persona.

---

**Created with ❤️ and 🧙‍♂️ wisdom**

