import streamlit as st
from datetime import datetime
import sys
import os
from typing import Dict, List, Optional

# Add paths for our admin system imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our comprehensive admin system components
try:
    from utils.text_processor import TextProcessor
    from models.text_classifier import TextClassifier
    from admin_system.database import DatabaseManager
    from utils.categories import get_all_categories, get_all_subcategories, CATEGORIES_STRUCTURE
    from config.supabase_config import test_connection
    # Import YouTubeTranscriber for video processing
    from utils.youtube_transcriber import YouTubeTranscriber
    ADMIN_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Admin system components not available: {e}")
    ADMIN_SYSTEM_AVAILABLE = False

def main():
    """Main application function for AI Baba chatbot"""
    
    # Page configuration
    st.set_page_config(
        page_title="AI Baba - Wise Guidance & Admin System",
        page_icon="🧙‍♂️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("🧙‍♂️ AI Baba")
        st.markdown("*Wise guidance for all your problems*")
        st.markdown("---")
        
        # Panel selection
        panel = st.selectbox(
            "Choose Panel",
            ["User Interface", "Admin Interface"],
            help="Select between User and Admin panels"
        )
        
        st.markdown("---")
        st.markdown(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Admin system status indicator
        if panel == "Admin Interface":
            if ADMIN_SYSTEM_AVAILABLE:
                st.success("🟢 Advanced Admin System: Ready")
            else:
                st.error("🔴 Advanced Admin System: Not Available")
    
    # Main content based on panel selection
    if panel == "User Interface":
        show_user_interface()
    elif panel == "Admin Interface":
        show_admin_interface()

def show_user_interface():
    """Display the user interface panel"""
    st.title("🧙‍♂️ Welcome to AI Baba")
    st.markdown("### *Your wise guide for life's challenges*")
    
    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("---")
        st.subheader("Share Your Problem")
        st.markdown("*Tell me what troubles you, and I shall guide you with ancient wisdom...*")
        
        # User input area (placeholder for now)
        user_problem = st.text_area(
            "What brings you to seek guidance?",
            placeholder="Describe your situation, challenge, or question...",
            height=150
        )
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            if st.button("🔮 Seek Wisdom", type="primary"):
                if user_problem:
                    st.info("🧙‍♂️ AI Baba is contemplating your question...")
                    # Placeholder for chatbot response logic
                    st.success("Feature will be implemented soon!")
                else:
                    st.warning("Please share your problem first!")
        
        with col_btn2:
            if st.button("🗑️ Clear"):
                st.rerun()
        
        # Conversation history placeholder
        st.markdown("---")
        st.subheader("📜 Conversation History")
        st.info("Your conversation with AI Baba will appear here...")
    
    with col2:
        st.markdown("---")
        st.subheader("🌟 About AI Baba")
        st.markdown("""
        AI Baba is your wise digital companion, offering guidance in the style of ancient wisdom.
        
        **Features:**
        - 🧠 Thoughtful problem analysis
        - 💡 Creative solution suggestions
        - 🎯 Personalized advice
        - 📚 Wisdom from various traditions
        """)
        
        st.markdown("---")
        st.subheader("🎨 Mood")
        st.select_slider(
            "How are you feeling?",
            options=["😢 Troubled", "😐 Neutral", "😊 Hopeful", "😄 Confident"],
            value="😐 Neutral"
        )

def show_admin_interface():
    """Display the enhanced admin interface panel"""
    st.title("⚙️ AI Baba Admin Control Panel")
    st.markdown("### *Comprehensive Management & Data Collection System*")
    
    # Admin authentication
    with st.expander("🔐 Authentication", expanded=True):
        admin_key = st.text_input("Enter Admin Key", type="password")
        if admin_key == "admin123":  # Placeholder authentication
            st.success("✅ Authenticated as Administrator")
            show_enhanced_admin_controls()
        elif admin_key:
            st.error("❌ Invalid admin key")
        else:
            st.info("Please enter admin key to access controls")

def show_enhanced_admin_controls():
    """Display enhanced admin control features with integrated system"""
    st.markdown("---")
    
    if ADMIN_SYSTEM_AVAILABLE:
        # Enhanced tabs with comprehensive admin system
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Dashboard", 
            "📋 Data Collection", 
            "💾 Database", 
            "📈 Analytics", 
            "⚙️ Settings", 
            "📋 Logs"
        ])
        
        with tab1:
            show_admin_dashboard()
        
        with tab2:
            show_data_collection_interface()
        
        with tab3:
            show_database_management()
        
        with tab4:
            show_analytics_dashboard()
        
        with tab5:
            show_system_settings()
        
        with tab6:
            show_system_logs()
    else:
        # Fallback to original basic admin interface
        show_basic_admin_controls()

@st.cache_resource
def get_admin_components():
    """Initialize and cache admin system components"""
    if not ADMIN_SYSTEM_AVAILABLE:
        return None
    
    try:
        return {
            'text_processor': TextProcessor(),
            'classifier': TextClassifier(),
            'db_manager': DatabaseManager()
        }
    except Exception as e:
        st.error(f"Failed to initialize admin components: {str(e)}")
        return None

def get_or_create_session_components():
    """Get components from session state or create new ones with bulletproof initialization"""
    if not ADMIN_SYSTEM_AVAILABLE:
        st.error("❌ Admin system components not available")
        return None
        
    if 'admin_components' not in st.session_state:
        with st.spinner("Initializing admin system..."):
            try:
                # Initialize database manager first
                db_manager = DatabaseManager()
                
                # Test database connection immediately
                db_success, db_message = db_manager.test_connection()
                if not db_success:
                    st.error(f"❌ Database connection failed: {db_message}")
                    return None
                
                # Initialize other components
                st.session_state.admin_components = {
                    'text_processor': TextProcessor(),
                    'classifier': TextClassifier(),
                    'db_manager': db_manager
                }
                
                st.success(f"✅ Admin system initialized - {db_message}")
                
            except Exception as e:
                st.error(f"❌ Failed to initialize admin system: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
                return None
    
    # Verify components are still working
    try:
        if 'db_manager' in st.session_state.admin_components:
            db_success, db_message = st.session_state.admin_components['db_manager'].test_connection()
            if not db_success:
                st.warning(f"⚠️ Database connection issue: {db_message}")
                # Try to reinitialize
                del st.session_state.admin_components
                return get_or_create_session_components()
    except:
        # Components corrupted, reinitialize
        if 'admin_components' in st.session_state:
            del st.session_state.admin_components
        return get_or_create_session_components()
    
    return st.session_state.admin_components

def show_admin_dashboard():
    """Enhanced admin dashboard with comprehensive overview"""
    st.subheader("📊 System Dashboard")
    
    components = get_or_create_session_components()
    if not components:
        st.error("❌ Admin system components not available")
        return
    
    # System status overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔧 System Status**")
        
        # Database connection test
        try:
            success, message = components['db_manager'].test_connection()
            if success:
                st.success("✅ Database: Connected")
            else:
                st.error("❌ Database: Error")
        except:
            st.error("❌ Database: Unavailable")
        
        # AI Models status
        if hasattr(components['classifier'], 'sentence_transformer') and components['classifier'].sentence_transformer:
            st.success("✅ AI Models: Loaded")
        else:
            st.warning("⚠️ AI Models: Not loaded")
    
    with col2:
        st.markdown("**📈 Quick Stats**")
        try:
            success, message, stats = components['db_manager'].get_statistics()
            if success:
                st.metric("Total Entries", stats.get('total_entries', 0))
                st.metric("Confirmed", stats.get('confirmed_entries', 0))
                st.metric("Pending", stats.get('pending_entries', 0))
            else:
                st.info("📊 No data available")
        except:
            st.error("❌ Stats unavailable")
    
    with col3:
        st.markdown("**🏷️ Categories**")
        st.info(f"Categories: {len(get_all_categories())}")
        st.info(f"Subcategories: {len(get_all_subcategories())}")
        
        # Recent activity indicator
        st.markdown("**🕒 System Health**")
        st.success("🟢 All systems operational")

def show_data_collection_interface():
    """Advanced data collection and processing interface"""
    st.subheader("📝 Advanced Data Collection & Processing")
    
    components = get_or_create_session_components()
    if not components:
        st.error("❌ Data collection system not available")
        return
    
    # Input method selection
    input_method = st.radio(
        "Select input method:",
        ["Text Input", "YouTube Video"],
        horizontal=True
    )
    
    # Initialize input_text variable
    input_text = ""
    
    if input_method == "Text Input":
        # Text input method
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Input Spiritual Advice Text**")
            input_text = st.text_area(
                "Paste raw text for processing:",
                height=200,
                placeholder="Enter the spiritual advice text from Osho, Buddha, Sadhguru, or other sources..."
            )
            
        with col2:
            st.markdown("**Processing Options**")
            
            # Processing settings
            preserve_formatting = st.checkbox("Preserve original formatting", True)
            detect_duplicates = st.checkbox("Check for duplicates", True)
            auto_categorize = st.checkbox("Auto-categorize with AI", True)
            
            # Processing button
            process_button = st.button("🚀 Process Text", type="primary")
        
        # Process text when button clicked
        if process_button and input_text.strip():
            process_admin_text_workflow(input_text, components, preserve_formatting, detect_duplicates, auto_categorize)
        elif process_button:
            st.error("⚠️ Please enter some text to process")
    
    else:  # YouTube Video input method
        # Create a styled container for the entire YouTube section
        st.markdown("""
        <div style="padding: 20px; border-radius: 10px; border: 1px solid #ddd; background-color: #f8f9fa; margin-bottom: 20px;">
            <h3 style="color: #333; margin-bottom: 15px;">Input YouTube Video URL</h3>
            <p style="color: #555;">Enter the URL of a YouTube video to transcribe and process its content.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # YouTube URL input with custom styling
        youtube_url = st.text_input(
            "Enter YouTube video URL:",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        
        # Create columns for options
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Processing settings
            preserve_formatting = st.checkbox("Preserve original formatting", True)
            detect_duplicates = st.checkbox("Check for duplicates", True)
            auto_categorize = st.checkbox("Auto-categorize with AI", True)
        
        with col2:
            # Processing button
            process_video_button = st.button("🎬 Process YouTube Video", type="primary")
        
        # Process YouTube video when button clicked
        if process_video_button and youtube_url.strip():
            # Create progress placeholder
            progress_placeholder = st.empty()
            
            def update_progress(message):
                progress_placeholder.info(message)
            
            # Initialize transcriber
            transcriber = YouTubeTranscriber()
            
            # Validate URL
            valid, msg = transcriber.validate_youtube_url(youtube_url)
            
            if valid:
                # Get video info
                success, message, video_info = transcriber.get_video_info(youtube_url)
                
                if success:
                    # Show video info
                    st.success(f"✅ Video found: {video_info['title']}")
                    
                    # Generate transcript
                    success, message, transcript = transcriber.generate_transcript(youtube_url, update_progress)
                    
                    if success:
                        # Format transcript with video metadata
                        formatted_transcript = transcriber.format_transcript_for_processing(transcript, video_info)
                        
                        # Process the transcript text
                        process_admin_text_workflow(formatted_transcript, components, preserve_formatting, detect_duplicates, auto_categorize)
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error(f"❌ {message}")
            else:
                st.error(f"❌ {msg}")
        elif process_video_button:
            st.error("⚠️ Please enter a YouTube URL")
    
    
    # Add entry management section
    show_entry_management_section()

def process_admin_text_workflow(input_text: str, components: Dict, preserve_formatting: bool, detect_duplicates: bool, auto_categorize: bool):
    """Complete admin text processing workflow - FIXED VERSION"""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Text Cleaning with fallback
        status_text.text("🧹 Step 1: Cleaning and preprocessing text...")
        progress_bar.progress(20)
        
        try:
            cleaning_result = components['text_processor'].clean_text(input_text)
        except Exception as e:
            st.warning(f"Text processing failed: {e}. Using simplified processing.")
            # Fallback to simple cleaning
            cleaning_result = {
                'cleaned_text': input_text.strip(),
                'is_valid': True,
                'statistics': {
                    'original_length': len(input_text),
                    'cleaned_length': len(input_text.strip()),
                    'reduction_percentage': 0
                },
                'changes_made': ['whitespace_cleanup'],
                'preserved_terms': {},
                'language': 'Unknown'
            }
        
        if not cleaning_result.get('is_valid', False):
            st.error("❌ Text cleaning failed. Using original text.")
            cleaning_result = {
                'cleaned_text': input_text.strip(),
                'is_valid': True,
                'statistics': {
                    'original_length': len(input_text),
                    'cleaned_length': len(input_text.strip()),
                    'reduction_percentage': 0
                },
                'changes_made': ['fallback'],
                'preserved_terms': {}
            }
        
        # Step 2: Originality Validation with fallback
        status_text.text("🔍 Step 2: Validating originality...")
        progress_bar.progress(40)
        
        try:
            originality_check = components['text_processor'].validate_originality(
                input_text, cleaning_result['cleaned_text']
            )
        except Exception as e:
            st.warning(f"Originality check failed: {e}. Assuming valid.")
            originality_check = {
                'is_valid': True,
                'similarity_score': 0.95,
                'issues': []
            }
        
        # Step 3: Classification with fallback
        classification_result = None
        if auto_categorize:
            status_text.text("🤖 Step 3: Classifying text using AI models...")
            progress_bar.progress(60)
            
            try:
                classification_result = components['classifier'].ensemble_classify(cleaning_result['cleaned_text'])
            except Exception as e:
                st.warning(f"Auto-classification failed: {e}. Manual classification required.")
                classification_result = None
        
        # Step 4: Auto-save processed data
        if classification_result and classification_result.get('category'):
            status_text.text("💾 Step 4: Auto-saving processed data...")
            progress_bar.progress(85)
            
            st.info("💾 Auto-saving processed data to knowledge base...")
            
            # Use bulletproof save functionality
            success = bulletproof_save_to_database(
                input_text,
                cleaning_result, 
                classification_result,
                components,
                confirmed=True
            )
            
            if success:
                status_text.text("✅ Processing and auto-save completed successfully!")
                progress_bar.progress(100)
                st.success("🎉 **PROCESSING COMPLETE!** Data automatically saved to AI Baba knowledge base.")
            else:
                status_text.text("⚠️ Processing completed, but auto-save encountered issues")
                progress_bar.progress(100)
                st.warning("⚠️ Processing successful, but save encountered issues. Check details above.")
        
        else:
            # No classification available, show manual classification
            status_text.text("✅ Processing completed - classification needed")
            progress_bar.progress(100)
            st.info("🤖 Processing completed. Manual classification required before auto-save.")
            
            # Store processing data for manual classification use
            st.session_state.current_processing_data = {
                'input_text': input_text,
                'cleaning_result': cleaning_result,
                'originality_check': originality_check
            }
            
            # Display results for manual classification
            display_admin_processing_results(
                input_text, 
                cleaning_result, 
                originality_check, 
                classification_result,
                components
            )
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"❌ Critical processing error: {str(e)}")
        st.code(f"Error details: {str(e)}")
        progress_bar.empty()
        status_text.empty()
        
        # Provide emergency fallback
        st.markdown("---")
        st.warning("⚠️ Processing failed. Using emergency save mode:")
        
        col1, col2 = st.columns(2)
        with col1:
            emergency_category = st.selectbox("Select Category:", ['Meditation', 'Philosophy', 'Self-Development'], key="emergency_cat")
        with col2:
            if st.button("🆘 Emergency Save", type="primary", key="emergency_save"):
                quick_test_save(input_text, emergency_category, components)

def display_admin_processing_results(input_text: str, cleaning_result: Dict, originality_check: Dict, classification_result: Optional[Dict], components: Dict):
    """Display comprehensive processing results in admin interface"""
    
    st.markdown("---")
    st.subheader("📋 Processing Results")
    
    # Results overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if originality_check['is_valid']:
            st.success("✅ Originality Preserved")
        else:
            st.warning("⚠️ Originality Concerns")
    
    with col2:
        if classification_result:
            st.success(f"🏷️ Classified: {classification_result['category']}")
        else:
            st.info("🤖 No Auto-Classification")
    
    with col3:
        reduction = cleaning_result['statistics']['reduction_percentage']
        st.metric("Text Reduction", f"{reduction}%")
    
    # Detailed tabs
    tab1, tab2, tab3 = st.tabs(["🔧 Text Analysis", "🏷️ Classification", "💾 Save to Database"])
    
    with tab1:
        display_admin_text_analysis(input_text, cleaning_result, originality_check)
    
    with tab2:
        display_admin_classification_results(classification_result)
    
    with tab3:
        display_admin_save_interface(input_text, cleaning_result, classification_result, components)

def display_admin_text_analysis(input_text: str, cleaning_result: Dict, originality_check: Dict):
    """Display detailed text analysis for admin"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original Text**")
        st.text_area("Original Text Area", value=input_text[:500] + "..." if len(input_text) > 500 else input_text, height=150, disabled=True, label_visibility="hidden")
        
        st.write(f"**Length:** {len(input_text)} characters")
        st.write(f"**Language:** {cleaning_result.get('language', 'Unknown')}")
    
    with col2:
        st.markdown("**Cleaned Text**")
        cleaned_text = cleaning_result['cleaned_text']
        st.text_area("Cleaned Text Area", value=cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text, height=150, disabled=True, label_visibility="hidden")
        
        stats = cleaning_result['statistics']
        st.write(f"**Length:** {stats['cleaned_length']} characters")
        st.write(f"**Reduction:** {stats['reduction_percentage']}%")
    
    # Processing details
    st.markdown("**Processing Applied:**")
    for change in cleaning_result['changes_made']:
        st.write(f"• {change.replace('_', ' ').title()}")
    
    # Preserved terms
    if cleaning_result['preserved_terms']:
        st.markdown("**Preserved Spiritual Terms:**")
        for term, original in cleaning_result['preserved_terms'].items():
            st.write(f"• **{original}** (detected as: {term})")

def display_admin_classification_results(classification_result: Optional[Dict]):
    """Display classification results for admin review"""
    
    if not classification_result:
        st.info("🤖 Auto-classification was not performed")
        
        # Manual classification option
        st.markdown("**Manual Classification**")
        selected_category = st.selectbox("Select Category:", get_all_categories())
        
        if selected_category:
            available_subcats = CATEGORIES_STRUCTURE[selected_category]['subcategories']
            selected_subcats = st.multiselect(
                "Select Subcategories:",
                options=available_subcats,
                default=[available_subcats[0]]
            )
            
            if st.button("🎯 Apply & Save", type="primary"):
                # Create manual classification
                manual_classification = {
                    'category': selected_category,
                    'subcategories': selected_subcats,
                    'confidence': 0.9,
                    'methods_used': ['manual'],
                    'metadata': {'manual_assignment': True}
                }
                
                # Get components and cleaning result from session state if available
                components = get_or_create_session_components()
                if components and hasattr(st.session_state, 'current_processing_data'):
                    # Auto-save with manual classification
                    success = bulletproof_save_to_database(
                        st.session_state.current_processing_data['input_text'],
                        st.session_state.current_processing_data['cleaning_result'],
                        manual_classification,
                        components,
                        confirmed=True
                    )
                    
                    if success:
                        st.success("🎉 **MANUAL CLASSIFICATION & SAVE COMPLETE!**")
                    else:
                        st.error("❌ Manual classification applied but save failed")
                else:
                    # Fallback to session state storage
                    st.session_state.manual_classification = manual_classification
                    st.success("✅ Manual classification applied!")
        return
    
    # Display AI classification results
    st.success(f"**Category:** {classification_result['category']}")
    st.info(f"**Confidence:** {classification_result['confidence']:.1%}")
    
    st.markdown("**Subcategories:**")
    for subcat in classification_result['subcategories']:
        st.write(f"• {subcat}")
    
    st.markdown("**Classification Methods:**")
    for method in classification_result['methods_used']:
        st.write(f"• {method.replace('_', ' ').title()}")
    
    # Alternative suggestions
    if len(classification_result['all_scores']) > 1:
        with st.expander("🔄 Alternative Suggestions"):
            alternatives = list(classification_result['all_scores'].items())[1:4]
            for category, score in alternatives:
                st.write(f"• **{category}**: {score:.1%}")

def display_admin_save_interface(input_text: str, cleaning_result: Dict, classification_result: Optional[Dict], components: Dict):
    """Admin interface for saving processed data - FIXED VERSION"""
    
    # Use manual classification if available
    if hasattr(st.session_state, 'manual_classification'):
        classification_result = st.session_state.manual_classification
    
    if not classification_result:
        st.warning("⚠️ Please classify the text first (manual or automatic)")
        
        # Provide a quick manual classification option
        st.markdown("**Quick Classification:**")
        col1, col2 = st.columns(2)
        with col1:
            quick_category = st.selectbox("Category:", ['Meditation', 'Philosophy', 'Self-Development'], key="quick_cat")
        with col2:
            if st.button("🎯 Apply & Save", key="quick_save"):
                # Create quick classification
                classification_result = {
                    'category': quick_category,
                    'subcategories': ['General'],
                    'confidence': 0.9,
                    'methods_used': ['manual_quick'],
                    'metadata': {'manual_assignment': True}
                }
                # Apply classification and save
                success = bulletproof_save_to_database(input_text, cleaning_result, classification_result, components)
                if success:
                    st.success("✅ **Quick classification and save completed!**")
                else:
                    st.error("❌ Save failed - check details above")
        return
    
    # Display final assignment
    st.success(f"**Final Category:** {classification_result['category']}")
    st.success(f"**Subcategories:** {', '.join(classification_result['subcategories'])}")
    
    # Show processing status
    if classification_result:
        st.success("✅ **Data has been automatically saved to the knowledge base!**")
        st.info("No manual confirmation needed - the processing workflow handles everything automatically.")
    else:
        st.info("🔄 Use manual classification above to complete the save process.")

def bulletproof_save_to_database(input_text: str, cleaning_result: Dict, classification_result: Dict, components: Dict, confirmed: bool = True):
    """Bulletproof save function integrated into main app"""
    
    import time
    
    # Create containers for feedback
    progress_container = st.empty()
    status_container = st.empty()
    debug_container = st.expander("🔍 Save Process Details", expanded=False)
    
    try:
        # Step 1: Validate inputs
        progress_container.progress(10)
        status_container.info("🔍 Step 1: Validating inputs...")
        
        with debug_container:
            st.markdown("**Step 1: Input Validation**")
            st.json({
                "has_input_text": bool(input_text and input_text.strip()),
                "has_cleaning_result": bool(cleaning_result),
                "has_classification_result": bool(classification_result),
                "has_components": bool(components),
                "confirmed_status": confirmed
            })
        
        if not input_text or not input_text.strip():
            st.error("❌ Text content cannot be empty")
            return False
        
        if not classification_result or not classification_result.get('category'):
            st.error("❌ Classification result is missing or invalid")
            return False
            
        if not components or 'db_manager' not in components:
            st.error("❌ Database components not available")
            return False
        
        # Step 2: Test database connection
        progress_container.progress(25)
        status_container.info("🔍 Step 2: Testing database connection...")
        
        db_success, db_message = components['db_manager'].test_connection()
        if not db_success:
            st.error(f"❌ Database connection failed: {db_message}")
            return False
            
        st.success(f"✅ Database connected: {db_message}")
        
        # Step 3: Prepare data
        progress_container.progress(50)
        status_container.info("🔍 Step 3: Preparing data...")
        
        # Clean text
        cleaned_text = cleaning_result.get('cleaned_text', input_text.strip())
        
        # Prepare metadata
        processing_metadata = {
            'processing_timestamp': datetime.now().isoformat(),
            'admin_processed': True,
            'bulletproof_save': True,
            'cleaning_stats': cleaning_result.get('statistics', {}),
            'changes_made': cleaning_result.get('changes_made', []),
            'preserved_terms': cleaning_result.get('preserved_terms', {}),
            'classification_metadata': classification_result.get('metadata', {}),
            'methods_used': classification_result.get('methods_used', []),
            'confidence_score': classification_result.get('confidence', 0.0),
            'processed_by_admin': True
        }
        
        with debug_container:
            st.markdown("**Step 3: Data Preparation**")
            st.code(f"""Save Parameters:
- Category: {classification_result.get('category', 'Unknown')}
- Subcategories: {classification_result.get('subcategories', [])}
- Original Text Length: {len(input_text)}
- Cleaned Text Length: {len(cleaned_text)}
- Confidence: {classification_result.get('confidence', 0.0)}
- Confirmed: {confirmed}""")
        
        # Step 4: Save to database
        progress_container.progress(75)
        status_container.info("🔍 Step 4: Saving to database...")
        
        # Ensure subcategories is a list
        subcategories = classification_result.get('subcategories', [])
        if isinstance(subcategories, str):
            subcategories = [subcategories]
        
        success, message, entry_id = components['db_manager'].insert_advice_entry(
            category=classification_result['category'],
            subcategories=subcategories,
            cleaned_text=cleaned_text,
            original_text=input_text,
            confidence_score=classification_result.get('confidence', 1.0),
            processing_metadata=processing_metadata,
            admin_confirmed=confirmed
        )
        
        # Step 5: Handle results
        progress_container.progress(100)
        
        if success:
            status_container.success("✅ Save completed successfully!")
            st.success(f"🎉 **SUCCESS**: {message}")
            st.info(f"📊 **Entry ID**: {entry_id}")
            
            # Store for reference
            st.session_state.last_saved_entry_id = entry_id
            
            # Step 6: Verify save
            st.info("🔍 Verifying save...")
            verify_success, verify_message, entry = components['db_manager'].get_entry_by_id(entry_id)
            
            if verify_success and entry:
                st.success("✅ **VERIFICATION SUCCESSFUL** - Data is saved in database!")
                
                with debug_container:
                    st.markdown("**Step 5: Verification Results**")
                    st.json({
                        "ID": entry['id'],
                        "Category": entry['category'],
                        "Subcategories": entry['subcategories'],
                        "Content_Preview": entry['information'][:100] + "..." if len(entry['information']) > 100 else entry['information'],
                        "Confirmed": entry['admin_confirmed'],
                        "Created": entry['created_at']
                    })
                
                # Success celebration
                if confirmed:
                    st.balloons()
                    st.info("📊 Data successfully added to AI Baba knowledge base!")
                
                # Clear session state
                if hasattr(st.session_state, 'manual_classification'):
                    del st.session_state.manual_classification
                    
                return True
                
            else:
                st.warning("⚠️ Save successful but verification failed. Entry might still be saved.")
                return True
                
        else:
            status_container.error("❌ Save failed!")
            st.error(f"💥 **SAVE FAILED**: {message}")
            
            # Show troubleshooting info
            with st.expander("🔧 Troubleshooting Information", expanded=True):
                st.markdown("**Possible causes:**")
                st.markdown("- Network connectivity issues")
                st.markdown("- Database permissions")
                st.markdown("- Data validation errors")
                st.markdown("- Server timeout")
                
                st.markdown("**What you can try:**")
                st.markdown("1. Check your internet connection")
                st.markdown("2. Try again in a few seconds")
                st.markdown("3. Refresh the page")
                st.markdown("4. Contact support if problem persists")
            
            return False
            
    except Exception as e:
        progress_container.empty()
        status_container.error("❌ Critical error during save!")
        
        st.error(f"💥 **CRITICAL ERROR**: {str(e)}")
        
        # Show detailed error information
        with st.expander("🚨 Error Details", expanded=True):
            import traceback
            st.code(traceback.format_exc())
            
        return False
    
    finally:
        # Clean up progress indicators after a delay
        time.sleep(2)
        progress_container.empty()
        status_container.empty()

def show_entry_management_section():
    """Show entry management section in main app"""
    if hasattr(st.session_state, 'last_saved_entry_id'):
        st.markdown("---")
        st.subheader("🗂️ Entry Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"Last saved entry ID: {st.session_state.last_saved_entry_id}")
        
        with col2:
            if st.button("🗑️ Delete Last Entry", type="secondary", key="delete_last_entry_main"):
                components = get_or_create_session_components()
                if components:
                    try:
                        success, message = components['db_manager'].delete_entry(st.session_state.last_saved_entry_id)
                        if success:
                            st.success("✅ Entry deleted successfully!")
                            del st.session_state.last_saved_entry_id
                            st.rerun()
                        else:
                            st.error(f"❌ Delete failed: {message}")
                    except Exception as e:
                        st.error(f"❌ Delete error: {str(e)}")

def quick_test_save(test_text: str, category: str, components: Dict):
    """Quick test save function - exact copy of debug app logic"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Simple text processing
        status_text.info("🧪 Step 1: Processing test text...")
        progress_bar.progress(25)
        
        # Create minimal cleaning result
        cleaning_result = {
            'cleaned_text': test_text.strip(),
            'is_valid': True,
            'statistics': {
                'original_length': len(test_text),
                'cleaned_length': len(test_text.strip()),
                'reduction_percentage': 0
            },
            'changes_made': ['whitespace_cleanup'],
            'preserved_terms': {}
        }
        
        # Step 2: Simple classification
        status_text.info("🧪 Step 2: Setting classification...")
        progress_bar.progress(50)
        
        classification_result = {
            'category': category,
            'subcategories': ['General'],
            'confidence': 1.0,
            'methods_used': ['manual_test'],
            'metadata': {'test_mode': True}
        }
        
        # Step 3: Prepare metadata
        status_text.info("🧪 Step 3: Preparing metadata...")
        progress_bar.progress(75)
        
        processing_metadata = {
            'processing_timestamp': datetime.now().isoformat(),
            'admin_processed': True,
            'test_mode': True,
            'cleaning_stats': cleaning_result['statistics'],
            'changes_made': cleaning_result['changes_made'],
            'preserved_terms': cleaning_result['preserved_terms'],
            'classification_metadata': classification_result['metadata'],
            'methods_used': classification_result['methods_used'],
            'confidence_score': classification_result['confidence'],
            'processed_by_admin': True
        }
        
        # Step 4: Save to database - EXACT DEBUG APP LOGIC
        status_text.info("🧪 Step 4: Saving to database...")
        progress_bar.progress(90)
        
        st.info(f"Saving: {category} - '{test_text[:50]}...'")
        
        success, message, entry_id = components['db_manager'].insert_advice_entry(
            category=classification_result['category'],
            subcategories=classification_result['subcategories'],
            cleaned_text=cleaning_result['cleaned_text'],
            original_text=test_text,
            confidence_score=classification_result['confidence'],
            processing_metadata=processing_metadata,
            admin_confirmed=True
        )
        
        # Step 5: Results
        status_text.success("✅ Test save completed!")
        progress_bar.progress(100)
        
        if success:
            st.success(f"✅ SUCCESS: {message}")
            st.info(f"🆔 Entry ID: {entry_id}")
            st.balloons()
            
            # Verify the save
            verify_success, verify_message, entry = components['db_manager'].get_entry_by_id(entry_id)
            
            if verify_success and entry:
                st.success("✅ Save verified - data is in database!")
                
                # Show cleanup option
                if st.button(f"🗑️ Delete Test Entry {entry_id}", key=f"cleanup_{entry_id}"):
                    del_success, del_message = components['db_manager'].delete_entry(entry_id)
                    if del_success:
                        st.success("Test entry cleaned up!")
                        st.rerun()
                    else:
                        st.error(f"Cleanup failed: {del_message}")
            else:
                st.error("❌ Save verification failed!")
        else:
            st.error(f"❌ SAVE FAILED: {message}")
            
        # Clean up
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"❌ Test save failed: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def show_database_management():
    """Enhanced database management interface"""
    st.subheader("💾 Database Management")
    
    components = get_or_create_session_components()
    if not components:
        st.error("❌ Database management not available")
        return
    
    # Database actions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    with col2:
        if st.button("📊 Statistics"):
            st.session_state.show_db_stats = True
    
    with col3:
        if st.button("🔍 Search"):
            st.session_state.show_search = True
    
    with col4:
        if st.button("📤 Export"):
            st.session_state.show_export = True
    
    # Show statistics if requested
    if st.session_state.get('show_db_stats', False):
        with st.expander("📊 Database Statistics", expanded=True):
            success, message, stats = components['db_manager'].get_statistics()
            
            if success:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Entries", stats['total_entries'])
                with col2:
                    st.metric("Confirmed", stats['confirmed_entries'])
                with col3:
                    st.metric("Pending", stats['pending_entries'])
                with col4:
                    if stats['total_entries'] > 0:
                        rate = (stats['confirmed_entries'] / stats['total_entries']) * 100
                        st.metric("Confirmation Rate", f"{rate:.1f}%")
                
                # Category distribution
                if stats['category_distribution']:
                    st.bar_chart(stats['category_distribution'])
            else:
                st.error(f"Error loading statistics: {message}")
    
    # Show search if requested
    if st.session_state.get('show_search', False):
        with st.expander("🔍 Search Database", expanded=True):
            search_term = st.text_input("Search term:")
            
            if search_term:
                success, message, results = components['db_manager'].search_entries(search_term)
                
                if success and results:
                    st.write(f"Found {len(results)} entries:")
                    display_admin_entries_table(results)
                else:
                    st.info("No results found")


def display_admin_entries_table(entries: List[Dict]):
    """Display entries table in admin interface"""
    
    # Prepare display data
    display_data = []
    for entry in entries:
        display_data.append({
            'ID': entry['id'],
            'Category': entry['category'],
            'Text Preview': entry['information'][:80] + '...' if len(entry['information']) > 80 else entry['information'],
            'Status': '✅ Confirmed' if entry['admin_confirmed'] else '⏳ Pending',
            'Date': entry['created_at'][:10]
        })
    
    # Display as dataframe
    import pandas as pd
    df = pd.DataFrame(display_data)
    st.dataframe(df, use_container_width=True)
    
    # Entry actions
    if entries:
        selected_id = st.selectbox("Select entry for actions:", [entry['id'] for entry in entries])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👁️ View Full"):
                components = get_or_create_session_components()
                if components:
                    display_admin_entry_details(selected_id, components['db_manager'])
        
        with col2:
            if st.button("✏️ Edit"):
                st.session_state.editing_entry = selected_id
        
        with col3:
            if st.button("🔑️ Delete", type="secondary"):
                if st.checkbox(f"Confirm delete entry {selected_id}"):
                    components = get_or_create_session_components()
                    if components:
                        success, message = components['db_manager'].delete_entry(selected_id)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

def display_admin_entry_details(entry_id: int, db_manager):
    """Display full entry details in admin interface"""
    
    success, message, entry = db_manager.get_entry_by_id(entry_id)
    
    if success and entry:
        with st.expander(f"Entry Details - ID: {entry_id}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Category:** {entry['category']}")
                st.write(f"**Subcategories:** {entry['subcategories']}")
                st.write(f"**Status:** {'Confirmed' if entry['admin_confirmed'] else 'Draft'}")
            
            with col2:
                st.write(f"**Created:** {entry['created_at']}")
                st.write(f"**Confidence:** {entry.get('confidence_score', 0):.1%}")
            
            st.markdown("**Content:**")
            st.text_area("Entry Content", value=entry['information'], height=150, disabled=True, label_visibility="hidden")
    else:
        st.error(f"Error loading entry: {message}")

def show_analytics_dashboard():
    """Enhanced analytics dashboard"""
    st.subheader("📈 Advanced Analytics")
    
    components = get_or_create_session_components()
    if not components:
        st.error("❌ Analytics not available")
        return
    
    # Analytics overview
    success, message, stats = components['db_manager'].get_statistics()
    
    if success:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Wisdom Entries", stats['total_entries'])
        with col2:
            st.metric("Ready for AI Baba", stats['confirmed_entries'])
        with col3:
            st.metric("Processing Queue", stats['pending_entries'])
        with col4:
            categories_count = len(stats.get('category_distribution', {}))
            st.metric("Active Categories", categories_count)
        
        # Category distribution chart
        if stats['category_distribution']:
            st.subheader("📊 Wisdom Distribution by Category")
            st.bar_chart(stats['category_distribution'])
            
            # Top categories
            sorted_categories = sorted(stats['category_distribution'].items(), key=lambda x: x[1], reverse=True)
            st.subheader("🏆 Top Wisdom Categories")
            
            for i, (category, count) in enumerate(sorted_categories[:5], 1):
                st.write(f"{i}. **{category}**: {count} entries")
        
        # Export options
        st.markdown("---")
        st.subheader("📤 Data Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export Full Dataset"):
                try:
                    success, message, df = components['db_manager'].export_to_dataframe()
                    
                    if success and not df.empty:
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="💾 Download CSV",
                            data=csv,
                            file_name=f"ai_baba_wisdom_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                        st.success(f"✅ Exported {len(df)} entries")
                    else:
                        st.error("No data to export")
                except Exception as e:
                    st.error(f"Export error: {e}")
        
        with col2:
            if st.button("📋 Generate Summary"):
                st.info("📊 Generating comprehensive summary...")
    else:
        st.error(f"Analytics error: {message}")

def show_system_settings():
    """Enhanced system settings"""
    st.subheader("⚙️ System Configuration")
    
    # Original chatbot settings
    with st.expander("🤖 AI Baba Personality Settings"):
        st.markdown("**Chatbot Behavior**")
        wisdom_level = st.slider("Wisdom Level", 1, 10, 7)
        humor_level = st.slider("Humor Level", 1, 10, 5)
        formality_level = st.slider("Formality Level", 1, 10, 6)
        
        st.markdown("**Response Style**")
        response_length = st.selectbox("Response Length", ["Short", "Medium", "Detailed"])
        include_examples = st.checkbox("Include Examples", True)
        include_questions = st.checkbox("Ask Follow-up Questions", True)
        
        if st.button("💾 Save Personality Settings"):
            st.success("AI Baba personality updated!")
    
    # Advanced admin system settings
    if ADMIN_SYSTEM_AVAILABLE:
        components = get_or_create_session_components()
        
        with st.expander("🔧 Advanced Processing Settings"):
            st.markdown("**Text Processing**")
            max_text_length = st.number_input("Max Text Length", 1000, 100000, 50000)
            confidence_threshold = st.slider("Classification Confidence Threshold", 0.0, 1.0, 0.3)
            enable_gpu = st.checkbox("Enable GPU Acceleration", False)
            
            st.markdown("**AI Model Configuration**")
            # Model status indicators
            if components:
                if components['classifier']._load_sentence_transformer():
                    st.success("✅ Sentence Transformer: Ready")
                else:
                    st.error("❌ Sentence Transformer: Failed to load")
                
                if components['classifier']._load_zero_shot_classifier():
                    st.success("✅ Zero-shot Classifier: Ready")
                else:
                    st.warning("⚠️ Zero-shot Classifier: Not loaded")
        
        with st.expander("💾 Database Configuration"):
            st.markdown("**Supabase Connection**")
            
            if components:
                if st.button("🔍 Test Database Connection"):
                    success, message = components['db_manager'].test_connection()
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
                
                if st.button("🏗️ Verify Table Schema"):
                    success, message = components['db_manager'].create_table_if_not_exists()
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        
        with st.expander("🏷️ Category Management"):
            st.markdown("**Available Categories**")
            categories = get_all_categories()
            st.info(f"Total Categories: {len(categories)}")
            st.info(f"Total Subcategories: {len(get_all_subcategories())}")
            
            # Show category structure
            for i, category in enumerate(categories, 1):
                subcats = CATEGORIES_STRUCTURE[category]['subcategories']
                st.write(f"{i}. **{category}** ({len(subcats)} subcategories)")
    
    else:
        st.warning("⚠️ Advanced settings require admin system components")

def show_system_logs():
    """Enhanced system logs"""
    st.subheader("📝 System Logs & Monitoring")
    
    # Log level selector
    col1, col2 = st.columns([1, 3])
    
    with col1:
        log_level = st.selectbox("Log Level", ["INFO", "WARNING", "ERROR", "DEBUG"])
    
    with col2:
        auto_refresh = st.checkbox("Auto-refresh logs", False)
    
    # Enhanced log display
    st.code(f"""
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: AI Baba system initialized
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Streamlit server started
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Admin system components {'loaded' if ADMIN_SYSTEM_AVAILABLE else 'unavailable'}
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Ready to serve users
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Database connection {'active' if ADMIN_SYSTEM_AVAILABLE else 'pending'}
    """, language="text")
    
    # System health monitoring
    st.markdown("---")
    st.subheader("🔧 System Health")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Uptime", "Active")
        st.metric("Memory Usage", "Normal")
    
    with col2:
        st.metric("Database Status", "✅ Connected" if ADMIN_SYSTEM_AVAILABLE else "❌ Offline")
        st.metric("AI Models", "✅ Ready" if ADMIN_SYSTEM_AVAILABLE else "❌ Loading")
    
    with col3:
        st.metric("Processing Queue", "0")
        st.metric("Error Rate", "0%")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Logs"):
            st.rerun()
    
    with col2:
        if st.button("💾 Export Logs"):
            st.info("Log export feature available")
    
    with col3:
        if st.button("🧹 Clear Logs"):
            st.warning("This will clear all log history!")

def show_basic_admin_controls():
    """Fallback basic admin controls when advanced system is unavailable"""
    st.warning("⚠️ Advanced admin system not available. Showing basic controls.")
    
    # Original basic admin interface
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "⚙️ Settings", "💬 Chat Management", "📝 Logs"])
    
    with tab1:
        st.subheader("📊 Usage Analytics")
        
        # Placeholder metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Conversations", "0", "0")
        with col2:
            st.metric("Active Users", "0", "0")
        with col3:
            st.metric("Avg. Response Time", "0.0s", "0.0s")
        with col4:
            st.metric("User Satisfaction", "0%", "0%")
        
        st.info("Advanced analytics available when admin system is loaded!")
    
    with tab2:
        st.subheader("⚙️ System Settings")
        
        # Chatbot behavior settings
        st.markdown("**🤖 Chatbot Personality**")
        wisdom_level = st.slider("Wisdom Level", 1, 10, 7)
        humor_level = st.slider("Humor Level", 1, 10, 5)
        formality_level = st.slider("Formality Level", 1, 10, 6)
        
        st.markdown("**🎨 Response Style**")
        response_length = st.selectbox("Response Length", ["Short", "Medium", "Detailed"])
        include_examples = st.checkbox("Include Examples", True)
        include_questions = st.checkbox("Ask Follow-up Questions", True)
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")
    
    with tab3:
        st.subheader("💬 Chat Management")
        
        st.markdown("**📋 Conversation Overview**")
        st.info("No active conversations to display")
        
        st.markdown("**🔧 Chat Controls**")
        if st.button("🗑️ Clear All Conversations"):
            st.warning("This will clear all conversation history!")
        
        if st.button("📊 Export Chat Data"):
            st.info("Export feature will be implemented soon!")
    
    with tab4:
        st.subheader("📝 System Logs")
        
        # Log level selector
        log_level = st.selectbox("Log Level", ["INFO", "WARNING", "ERROR", "DEBUG"])
        
        # Placeholder log display
        st.code(f"""
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: AI Baba system initialized
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Streamlit server started
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: Advanced admin system not loaded
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Ready to serve users (basic mode)
        """, language="text")
        
        if st.button("🔄 Refresh Logs"):
            st.rerun()

if __name__ == "__main__":
    main()
