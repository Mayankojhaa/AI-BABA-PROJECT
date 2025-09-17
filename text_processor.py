"""
Advanced text cleaning and preprocessing module for AI Baba admin system
Focuses on cleaning while preserving originality and meaning
"""
import re
import string
import unicodedata
from typing import List, Dict, Set, Tuple, Optional
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
from unidecode import unidecode
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException as LangDetectError
import hashlib

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class TextProcessor:
    """Advanced text cleaning and preprocessing with originality preservation"""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Try to load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def detect_language(self, text: str) -> str:
        """Detect language of the text"""
        try:
            return detect(text)
        except LangDetectError:
            return "unknown"
    
    def calculate_text_hash(self, text: str) -> str:
        """Calculate hash of text for duplicate detection"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace while preserving paragraph structure"""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple newlines with double newline (paragraph break)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Replace single newlines with space (except paragraph breaks)
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        
        return text.strip()
    
    def fix_encoding_issues(self, text: str) -> str:
        """Fix common encoding issues while preserving meaning"""
        # Handle Unicode normalization
        text = unicodedata.normalize('NFKC', text)
        
        # Fix common encoding issues
        encoding_fixes = {
            'â€™': "'",  # Smart apostrophe
            'â€œ': '"',  # Smart quote left
            'â€\x9d': '"',  # Smart quote right
            'â€¦': '...',  # Ellipsis
            'â€"': '—',  # Em dash
            'â€"': '–',  # En dash
            'Ã¡': 'á',
            'Ã©': 'é',
            'Ã­': 'í',
            'Ã³': 'ó',
            'Ãº': 'ú',
        }
        
        for bad, good in encoding_fixes.items():
            text = text.replace(bad, good)
        
        return text
    
    def clean_special_characters(self, text: str) -> str:
        """Clean special characters while preserving essential punctuation"""
        # Remove or replace problematic characters
        text = re.sub(r'[^\w\s.,!?;:()\-\'"]+', ' ', text)
        
        # Fix multiple punctuation
        text = re.sub(r'\.{3,}', '...', text)  # Multiple dots to ellipsis
        text = re.sub(r'[!]{2,}', '!', text)   # Multiple exclamations
        text = re.sub(r'[?]{2,}', '?', text)   # Multiple questions
        
        return text
    
    def remove_unwanted_patterns(self, text: str) -> str:
        """Remove unwanted patterns while preserving content"""
        patterns_to_remove = [
            r'\b(?:https?://|www\.)\S+',  # URLs
            r'\b\w+@\w+\.\w+\b',          # Email addresses
            r'\b\d{10,}\b',               # Long numbers (likely phone/ID)
            r'#\w+',                      # Hashtags
            r'@\w+',                      # Mentions
            r'\[.*?\]',                   # Text in square brackets
            r'<.*?>',                     # HTML tags
            r'\{.*?\}',                   # Text in curly braces
        ]
        
        for pattern in patterns_to_remove:
            text = re.sub(pattern, ' ', text, flags=re.IGNORECASE)
        
        return text
    
    def preserve_spiritual_terms(self, text: str) -> Dict[str, str]:
        """Identify and preserve spiritual/philosophical terms"""
        spiritual_terms = {
            'osho', 'buddha', 'sadhguru', 'meditation', 'karma', 'dharma',
            'enlightenment', 'consciousness', 'awareness', 'mindfulness',
            'spirituality', 'moksha', 'nirvana', 'brahman', 'atman',
            'yoga', 'pranayama', 'chakra', 'kundalini', 'mantra'
        }
        
        preserved_terms = {}
        text_lower = text.lower()
        
        for term in spiritual_terms:
            if term in text_lower:
                # Find all occurrences with original capitalization
                pattern = r'\b' + re.escape(term) + r'\b'
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    preserved_terms[term] = matches[0]  # Keep original capitalization
        
        return preserved_terms
    
    def clean_text(self, text: str) -> Dict[str, any]:
        """
        Comprehensive text cleaning while preserving originality
        
        Returns:
            Dictionary with cleaned text and metadata
        """
        original_text = text
        original_hash = self.calculate_text_hash(original_text)
        
        # Step 1: Basic validation
        if not text or not text.strip():
            return {
                'cleaned_text': '',
                'original_text': original_text,
                'original_hash': original_hash,
                'language': 'unknown',
                'changes_made': ['empty_text'],
                'preserved_terms': {},
                'statistics': {'original_length': 0, 'cleaned_length': 0},
                'is_valid': False
            }
        
        changes_made = []
        
        # Step 2: Language detection
        language = self.detect_language(text)
        
        # Step 3: Preserve important terms
        preserved_terms = self.preserve_spiritual_terms(text)
        
        # Step 4: Fix encoding issues
        original_len = len(text)
        text = self.fix_encoding_issues(text)
        if len(text) != original_len:
            changes_made.append('encoding_fixed')
        
        # Step 5: Normalize whitespace
        text = self.normalize_whitespace(text)
        changes_made.append('whitespace_normalized')
        
        # Step 6: Remove unwanted patterns
        text_before = text
        text = self.remove_unwanted_patterns(text)
        if text != text_before:
            changes_made.append('unwanted_patterns_removed')
        
        # Step 7: Clean special characters
        text_before = text
        text = self.clean_special_characters(text)
        if text != text_before:
            changes_made.append('special_characters_cleaned')
        
        # Step 8: Final whitespace cleanup
        text = self.normalize_whitespace(text)
        
        # Step 9: Validate result
        is_valid = len(text.strip()) > 0
        
        # Calculate statistics
        statistics = {
            'original_length': len(original_text),
            'cleaned_length': len(text),
            'reduction_percentage': round((1 - len(text) / len(original_text)) * 100, 2) if len(original_text) > 0 else 0,
            'language': language
        }
        
        return {
            'cleaned_text': text,
            'original_text': original_text,
            'original_hash': original_hash,
            'language': language,
            'changes_made': changes_made,
            'preserved_terms': preserved_terms,
            'statistics': statistics,
            'is_valid': is_valid
        }
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences while preserving structure"""
        try:
            sentences = sent_tokenize(text)
            # Filter out very short sentences (likely fragments)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
            return sentences
        except:
            # Fallback: split by periods
            sentences = text.split('.')
            return [s.strip() + '.' for s in sentences if len(s.strip()) > 10]
    
    def detect_duplicates(self, texts: List[str], similarity_threshold: float = 0.9) -> List[Dict]:
        """
        Detect duplicate texts based on similarity
        
        Args:
            texts: List of texts to check
            similarity_threshold: Similarity threshold for duplicates
            
        Returns:
            List of duplicate groups
        """
        duplicates = []
        text_hashes = {}
        
        for i, text in enumerate(texts):
            text_hash = self.calculate_text_hash(text.strip().lower())
            
            if text_hash in text_hashes:
                # Exact duplicate found
                duplicates.append({
                    'type': 'exact',
                    'original_index': text_hashes[text_hash],
                    'duplicate_index': i,
                    'similarity': 1.0
                })
            else:
                text_hashes[text_hash] = i
        
        return duplicates
    
    def batch_process_texts(self, texts: List[str]) -> List[Dict]:
        """Process multiple texts in batch"""
        results = []
        
        for i, text in enumerate(texts):
            try:
                result = self.clean_text(text)
                result['batch_index'] = i
                results.append(result)
            except Exception as e:
                results.append({
                    'cleaned_text': '',
                    'original_text': text,
                    'batch_index': i,
                    'error': str(e),
                    'is_valid': False
                })
        
        return results
    
    def get_text_statistics(self, text: str) -> Dict:
        """Get comprehensive text statistics"""
        sentences = self.extract_sentences(text)
        words = word_tokenize(text.lower())
        
        return {
            'character_count': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'average_sentence_length': round(len(words) / len(sentences), 2) if sentences else 0,
            'language': self.detect_language(text),
            'has_spiritual_terms': len(self.preserve_spiritual_terms(text)) > 0
        }
    
    def validate_originality(self, original: str, cleaned: str) -> Dict:
        """
        Validate that cleaning preserved originality
        
        Args:
            original: Original text
            cleaned: Cleaned text
            
        Returns:
            Validation results
        """
        # Extract key content words from both texts
        def get_content_words(text):
            words = word_tokenize(text.lower())
            content_words = [w for w in words if w not in self.stop_words and w.isalpha()]
            return set(content_words)
        
        original_words = get_content_words(original)
        cleaned_words = get_content_words(cleaned)
        
        # Calculate preservation metrics
        if original_words:
            preserved_ratio = len(original_words.intersection(cleaned_words)) / len(original_words)
        else:
            preserved_ratio = 1.0
        
        # Check for added content
        added_words = cleaned_words - original_words
        
        return {
            'originality_preserved': preserved_ratio >= 0.8,  # 80% threshold
            'content_preservation_ratio': round(preserved_ratio, 3),
            'words_preserved': len(original_words.intersection(cleaned_words)),
            'words_lost': len(original_words - cleaned_words),
            'words_added': len(added_words),
            'added_words': list(added_words)[:10],  # Show first 10 added words
            'is_valid': preserved_ratio >= 0.8 and len(added_words) == 0
        }

# Global instance for easy access
text_processor = TextProcessor()

def clean_text_simple(text: str) -> str:
    """Simple interface for text cleaning"""
    result = text_processor.clean_text(text)
    return result['cleaned_text']

def validate_text_originality(original: str, cleaned: str) -> bool:
    """Simple interface for originality validation"""
    result = text_processor.validate_originality(original, cleaned)
    return result['is_valid']
