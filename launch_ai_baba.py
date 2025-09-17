#!/usr/bin/env python3
"""
Enhanced AI Baba System Launcher
Launches the integrated AI Baba system with comprehensive admin capabilities
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if environment is properly set up"""
    print("🧿 AI Baba System Launcher")
    print("=" * 50)
    print("🔍 Checking environment setup...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("📋 Please copy .env.example to .env and configure your Supabase credentials")
        return False
    
    print("✅ Environment file found")
    
    # Check if required packages are installed
    required_packages = [
        'streamlit', 'supabase', 'transformers', 'torch', 'sentence-transformers',
        'scikit-learn', 'pandas', 'numpy', 'nltk', 'spacy', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("✅ Required packages installed")
    return True

def setup_nltk_data():
    """Download required NLTK data"""
    print("📥 Setting up NLTK data...")
    
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True) 
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data ready")
    except Exception as e:
        print(f"⚠️ NLTK data setup failed: {e}")

def setup_spacy_model():
    """Download spaCy English model"""
    print("📥 Checking spaCy model...")
    
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print("✅ spaCy model available")
        except OSError:
            print("📥 Downloading spaCy English model...")
            subprocess.run([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm"
            ], check=True)
            print("✅ spaCy model downloaded")
    except Exception as e:
        print(f"⚠️ spaCy model setup failed: {e}")
        print("💡 You can install manually: python -m spacy download en_core_web_sm")

def test_system():
    """Test system components"""
    print("⚙️ Testing system components...")
    
    try:
        # Test imports
        from utils.text_processor import TextProcessor
        from models.text_classifier import TextClassifier
        from admin_system.database import DatabaseManager
        from utils.categories import get_all_categories
        
        print("✅ Core components loaded")
        
        # Test categories
        categories = get_all_categories()
        print(f"✅ {len(categories)} categories available")
        
        return True
    except ImportError as e:
        print(f"❌ Component import error: {e}")
        return False

def launch_system():
    """Launch the integrated AI Baba system"""
    print("🚀 Launching AI Baba Integrated System...")
    print("🌐 The interface will open in your browser")
    print("🔧 Use Ctrl+C to stop the server")
    print("-" * 50)
    
    # Run Streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 AI Baba System stopped gracefully")
    except Exception as e:
        print(f"❌ Error launching system: {e}")

def display_system_info():
    """Display system information"""
    print("\n🧿 AI Baba Integrated System - Ready!")
    print("=" * 50)
    print("📋 System Features:")
    print("  🧙‍♂️ User Interface - Spiritual guidance chatbot")
    print("  ⚙️ Admin Interface - Comprehensive management system")
    print("    • 📝 Advanced text processing & cleaning")
    print("    • 🤖 AI-powered categorization")
    print("    • 💾 Supabase database integration")
    print("    • 📊 Analytics & reporting")
    print("    • 🔧 System management")
    print()
    print("🔑 Admin Access:")
    print("  1. Select 'Admin Interface' in the sidebar")
    print("  2. Enter admin key: admin123")
    print("  3. Access all 6 admin modules")
    print()
    print("🌐 Access URL: http://localhost:8501")
    print("=" * 50)

def main():
    """Main launcher function"""
    
    # Check environment
    if not check_environment():
        print("\n💡 Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Add your Supabase URL and API key")
        print("3. Run: pip install -r requirements.txt")
        print("4. Run this script again")
        return
    
    # Setup system
    setup_nltk_data()
    setup_spacy_model()
    
    if not test_system():
        print("❌ System component test failed")
        print("💡 Check if all files are in place and dependencies are installed")
        return
    
    # Display info
    display_system_info()
    
    # Launch system
    launch_system()

if __name__ == "__main__":
    main()
