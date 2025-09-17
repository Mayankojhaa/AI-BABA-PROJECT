# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

AI Baba is a conversational chatbot application built with Streamlit that provides wise guidance in a mystical, Baba-style persona. The project is currently in early development with placeholder UI components ready for AI integration.

## Technology Stack

- **Framework**: Streamlit (v1.28.0)
- **Language**: Python 3.8+
- **Dependencies**: pandas, numpy, python-dotenv
- **Environment**: Virtual environment (venv)
- **Authentication**: Simple password-based admin access

## Development Commands

### Environment Setup
```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start Streamlit development server
streamlit run app.py

# The app will be available at http://localhost:8501
```

### Development Tasks
```bash
# Install new dependencies and update requirements
pip install package_name
pip freeze > requirements.txt

# Check Python version compatibility
python --version

# Deactivate virtual environment
deactivate
```

## Application Architecture

### Single-File Architecture
The entire application is contained in `app.py` with a functional, tab-based structure:

- **main()**: Entry point with page config and sidebar navigation
- **show_user_interface()**: User-facing chat interface with placeholder functionality
- **show_admin_interface()**: Admin panel with authentication gate
- **show_admin_controls()**: Tabbed admin features (Analytics, Settings, Chat Management, Logs)

### Key Design Patterns

#### Panel-Based Navigation
The app uses Streamlit's selectbox in the sidebar to switch between User and Admin interfaces, implementing a simple single-page application pattern.

#### Session State Management
Currently uses Streamlit's built-in session state. All data is temporary and lost on page refresh - ready for database integration.

#### Authentication Pattern
Simple password-based check (`admin123`) in the admin interface. This is a placeholder for production authentication systems.

#### Tab-Based Admin Interface
Admin controls are organized into four main tabs:
- **Analytics**: Placeholder metrics and usage statistics
- **Settings**: Chatbot personality and response configuration
- **Chat Management**: Conversation oversight and data export
- **Logs**: System monitoring and debugging

### UI Component Structure

#### User Interface Components
- Two-column layout (chat area + info sidebar)
- Text area for user input with placeholder text
- Action buttons (Seek Wisdom, Clear)
- Mood tracking slider
- Conversation history placeholder

#### Admin Interface Components
- Expandable authentication section
- Tabbed control panels
- Metric cards for analytics
- Configuration sliders and checkboxes
- Code blocks for log display

## Development Notes

### Placeholder Functionality
Most core features are implemented as UI placeholders ready for backend integration:
- Chat functionality displays success messages instead of AI responses
- Analytics show zero metrics with proper structure
- Conversation history is informational text
- Log display uses static demo content

### Configuration Management
Admin settings are collected via UI controls but not persisted. Future implementations should:
- Store settings in configuration files or database
- Apply personality settings to AI model parameters
- Implement response length and style controls

### Authentication Security
Current admin authentication is basic and should be replaced with:
- Environment variable-based secrets
- Session-based authentication
- Role-based access control

### Styling and Theming
The application uses emoji-rich styling with mystical/ancient wisdom theme:
- 🧙‍♂️ for AI Baba branding
- Warm, encouraging language in UI text
- Consistent use of themed emojis throughout interface

## Integration Points

### AI Model Integration
The `show_user_interface()` function has a clear integration point in the "Seek Wisdom" button handler where AI processing should be implemented.

### Database Integration
Session state management is ready for replacement with persistent storage for:
- User conversations and history
- Admin configuration settings
- Analytics and usage metrics
- System logs and debugging information

### Authentication System
The admin authentication check in `show_admin_interface()` can be replaced with more robust authentication frameworks.

## File Structure Context

```
ai-baba/
├── app.py              # Complete Streamlit application
├── requirements.txt    # Python dependencies (streamlit, pandas, numpy, python-dotenv)
├── README.md          # Comprehensive project documentation
├── .gitignore         # Standard Python/Streamlit ignore patterns
└── venv/              # Virtual environment (gitignored)
```

## Important Constants and Configuration

- **Admin Key**: `admin123` (hardcoded in line 107 of app.py)
- **Default Port**: 8501 (Streamlit default)
- **Page Title**: "AI Baba - Wise Guidance Chatbot"
- **Page Icon**: "🧙‍♂️"
- **Layout**: Wide mode with expanded sidebar

## Future Development Priorities

Based on the README.md roadmap, the next major development phases should focus on:

1. **AI Integration**: Implement actual chatbot functionality with OpenAI, Anthropic, or local models
2. **Database Layer**: Add conversation persistence and user management
3. **Authentication System**: Replace placeholder admin auth with secure implementation  
4. **Analytics Backend**: Implement real metrics collection and reporting
5. **API Development**: Create endpoints for external integrations

When implementing these features, maintain the existing UI structure and placeholder patterns to ensure smooth integration.
