"""
AI-powered text categorization and classification system for AI Baba
Uses Hugging Face transformers, sentence transformers, and ML techniques
"""
import warnings
warnings.filterwarnings('ignore')

import os
import json
import numpy as np
from typing import List, Dict, Tuple, Optional
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import re

# Import our utilities
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.categories import (
    CATEGORIES_STRUCTURE, get_all_categories, get_all_subcategories,
    find_categories_by_keywords, CATEGORY_PROMPTS, validate_category_assignment
)

class TextClassifier:
    """Advanced text classification using multiple AI techniques"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Initialize models (lazy loading)
        self.sentence_transformer = None
        self.zero_shot_classifier = None
        self.tfidf_vectorizer = None
        self.lda_model = None
        self.category_embeddings = None
        
        # Categories for classification
        self.categories = get_all_categories()
        self.all_subcategories = get_all_subcategories()
        
    def _load_sentence_transformer(self):
        """Load sentence transformer model"""
        if self.sentence_transformer is None:
            try:
                self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
                print("Loaded sentence transformer model")
            except Exception as e:
                print(f"Error loading sentence transformer: {e}")
                self.sentence_transformer = None
        return self.sentence_transformer is not None
    
    def _load_zero_shot_classifier(self):
        """Load zero-shot classification model"""
        if self.zero_shot_classifier is None:
            try:
                self.zero_shot_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=0 if self.device == "cuda" else -1
                )
                print("Loaded zero-shot classification model")
            except Exception as e:
                print(f"Error loading zero-shot classifier: {e}")
                self.zero_shot_classifier = None
        return self.zero_shot_classifier is not None
    
    def _load_tfidf_vectorizer(self):
        """Initialize TF-IDF vectorizer"""
        if self.tfidf_vectorizer is None:
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.8
            )
        return True
    
    def precompute_category_embeddings(self):
        """Precompute embeddings for all categories and subcategories"""
        if not self._load_sentence_transformer():
            return False
        
        if self.category_embeddings is not None:
            return True
        
        try:
            # Create category descriptions for better embeddings
            category_texts = []
            category_labels = []
            
            for category, data in CATEGORIES_STRUCTURE.items():
                # Main category description
                prompt = CATEGORY_PROMPTS.get(category, f"This is about {category}")
                keywords = " ".join(data["keywords"][:10])  # Use top keywords
                category_text = f"{prompt} Keywords: {keywords}"
                
                category_texts.append(category_text)
                category_labels.append(f"main:{category}")
                
                # Subcategory descriptions
                for subcategory in data["subcategories"]:
                    subcat_text = f"{subcategory} in the context of {category}. {prompt}"
                    category_texts.append(subcat_text)
                    category_labels.append(f"sub:{subcategory}")
            
            # Generate embeddings
            embeddings = self.sentence_transformer.encode(category_texts)
            
            self.category_embeddings = {
                'embeddings': embeddings,
                'labels': category_labels,
                'texts': category_texts
            }
            
            print(f"Precomputed embeddings for {len(category_texts)} categories/subcategories")
            return True
            
        except Exception as e:
            print(f"Error precomputing embeddings: {e}")
            return False
    
    def classify_with_zero_shot(self, text: str, top_k: int = 3) -> List[Dict]:
        """Classify text using zero-shot classification"""
        if not self._load_zero_shot_classifier():
            return []
        
        try:
            # Classify main categories
            result = self.zero_shot_classifier(text, self.categories)
            
            classifications = []
            for label, score in zip(result['labels'][:top_k], result['scores'][:top_k]):
                classifications.append({
                    'category': label,
                    'confidence': float(score),
                    'method': 'zero_shot'
                })
            
            return classifications
            
        except Exception as e:
            print(f"Error in zero-shot classification: {e}")
            return []
    
    def classify_with_embeddings(self, text: str, top_k: int = 3) -> List[Dict]:
        """Classify text using sentence embeddings"""
        if not self._load_sentence_transformer():
            return []
        
        if not self.precompute_category_embeddings():
            return []
        
        try:
            # Get text embedding
            text_embedding = self.sentence_transformer.encode([text])
            
            # Calculate similarities
            similarities = cosine_similarity(text_embedding, self.category_embeddings['embeddings'])[0]
            
            # Get top matches
            top_indices = np.argsort(similarities)[-top_k*2:][::-1]  # Get more to filter
            
            classifications = []
            seen_categories = set()
            
            for idx in top_indices:
                label = self.category_embeddings['labels'][idx]
                similarity = float(similarities[idx])
                
                if label.startswith('main:'):
                    category = label.replace('main:', '')
                    if category not in seen_categories:
                        classifications.append({
                            'category': category,
                            'confidence': similarity,
                            'method': 'embedding'
                        })
                        seen_categories.add(category)
                
                if len(classifications) >= top_k:
                    break
            
            return classifications
            
        except Exception as e:
            print(f"Error in embedding classification: {e}")
            return []
    
    def classify_with_keywords(self, text: str, top_k: int = 3) -> List[Dict]:
        """Classify text using keyword matching"""
        try:
            keyword_scores = find_categories_by_keywords(text, threshold=1)
            
            classifications = []
            for category, score in list(keyword_scores.items())[:top_k]:
                # Normalize score (simple approach)
                confidence = min(score / 10.0, 1.0)  # Assume max 10 keywords
                classifications.append({
                    'category': category,
                    'confidence': confidence,
                    'method': 'keyword'
                })
            
            return classifications
            
        except Exception as e:
            print(f"Error in keyword classification: {e}")
            return []
    
    def classify_subcategories(self, text: str, main_category: str, top_k: int = 2) -> List[Dict]:
        """Classify text into subcategories within a main category"""
        if main_category not in CATEGORIES_STRUCTURE:
            return []
        
        subcategories = CATEGORIES_STRUCTURE[main_category]['subcategories']
        
        if not self._load_sentence_transformer():
            # Fallback to keyword matching for subcategories
            return self._classify_subcategories_keywords(text, main_category, top_k)
        
        try:
            # Create subcategory prompts
            subcategory_prompts = []
            for subcat in subcategories:
                prompt = f"This text is about {subcat} in the context of {main_category}"
                subcategory_prompts.append(prompt)
            
            # Get embeddings
            text_embedding = self.sentence_transformer.encode([text])
            subcat_embeddings = self.sentence_transformer.encode(subcategory_prompts)
            
            # Calculate similarities
            similarities = cosine_similarity(text_embedding, subcat_embeddings)[0]
            
            # Get top matches
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            classifications = []
            for idx in top_indices:
                subcategory = subcategories[idx]
                similarity = float(similarities[idx])
                
                # Only include if similarity is reasonable
                if similarity > 0.3:  # Threshold for subcategory matching
                    classifications.append({
                        'subcategory': subcategory,
                        'confidence': similarity,
                        'method': 'embedding'
                    })
            
            return classifications
            
        except Exception as e:
            print(f"Error in subcategory classification: {e}")
            return self._classify_subcategories_keywords(text, main_category, top_k)
    
    def _classify_subcategories_keywords(self, text: str, main_category: str, top_k: int = 2) -> List[Dict]:
        """Fallback subcategory classification using keywords"""
        subcategories = CATEGORIES_STRUCTURE[main_category]['subcategories']
        text_lower = text.lower()
        
        scores = {}
        for subcat in subcategories:
            score = 0
            subcat_words = re.findall(r'\w+', subcat.lower())
            
            for word in subcat_words:
                if word in text_lower:
                    score += 1
            
            if score > 0:
                scores[subcat] = score / len(subcat_words)  # Normalize by subcategory length
        
        # Sort and return top matches
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        classifications = []
        for subcat, score in sorted_scores[:top_k]:
            classifications.append({
                'subcategory': subcat,
                'confidence': min(score, 1.0),
                'method': 'keyword'
            })
        
        return classifications
    
    def ensemble_classify(self, text: str) -> Dict:
        """
        Classify text using ensemble of methods
        
        Returns:
            Dictionary with classification results
        """
        # Get classifications from different methods
        zero_shot_results = self.classify_with_zero_shot(text, top_k=3)
        embedding_results = self.classify_with_embeddings(text, top_k=3)
        keyword_results = self.classify_with_keywords(text, top_k=3)
        
        # Combine and weight results
        category_scores = {}
        
        # Weight different methods
        weights = {
            'zero_shot': 0.4,
            'embedding': 0.4,
            'keyword': 0.2
        }
        
        for results, method in [(zero_shot_results, 'zero_shot'), 
                               (embedding_results, 'embedding'), 
                               (keyword_results, 'keyword')]:
            weight = weights[method]
            for result in results:
                category = result['category']
                confidence = result['confidence']
                
                if category in category_scores:
                    category_scores[category] += confidence * weight
                else:
                    category_scores[category] = confidence * weight
        
        # Get best category
        if not category_scores:
            return {
                'category': 'General Curiosity & Learning',  # Default category
                'confidence': 0.1,
                'subcategories': ['Life Advice (general guidance)'],
                'methods_used': ['fallback'],
                'all_scores': {},
                'metadata': {
                    'zero_shot_available': len(zero_shot_results) > 0,
                    'embedding_available': len(embedding_results) > 0,
                    'keyword_matches': len(keyword_results) > 0
                }
            }
        
        best_category = max(category_scores.items(), key=lambda x: x[1])
        category_name = best_category[0]
        category_confidence = best_category[1]
        
        # Get subcategories for the best category
        subcategory_results = self.classify_subcategories(text, category_name, top_k=2)
        subcategories = [r['subcategory'] for r in subcategory_results if r['confidence'] > 0.3]
        
        # If no subcategories found, use default
        if not subcategories and category_name in CATEGORIES_STRUCTURE:
            subcategories = [CATEGORIES_STRUCTURE[category_name]['subcategories'][0]]
        
        methods_used = []
        if zero_shot_results:
            methods_used.append('zero_shot')
        if embedding_results:
            methods_used.append('embedding')
        if keyword_results:
            methods_used.append('keyword')
        
        return {
            'category': category_name,
            'confidence': min(category_confidence, 1.0),
            'subcategories': subcategories,
            'methods_used': methods_used,
            'all_scores': dict(sorted(category_scores.items(), key=lambda x: x[1], reverse=True)),
            'metadata': {
                'zero_shot_results': zero_shot_results[:2],
                'embedding_results': embedding_results[:2],
                'keyword_results': keyword_results[:2],
                'subcategory_results': subcategory_results
            }
        }
    
    def validate_classification(self, text: str, category: str, subcategories: List[str]) -> Dict:
        """Validate a classification result"""
        # Check if category exists
        if category not in CATEGORIES_STRUCTURE:
            return {
                'is_valid': False,
                'error': f'Invalid category: {category}',
                'suggestions': self.get_category_suggestions(text)
            }
        
        # Check if subcategories belong to category
        valid_subcategories = set(CATEGORIES_STRUCTURE[category]['subcategories'])
        invalid_subcats = [s for s in subcategories if s not in valid_subcategories]
        
        if invalid_subcats:
            return {
                'is_valid': False,
                'error': f'Invalid subcategories for {category}: {invalid_subcats}',
                'valid_subcategories': list(valid_subcategories)
            }
        
        return {
            'is_valid': True,
            'confidence_check': self._calculate_validation_confidence(text, category, subcategories)
        }
    
    def _calculate_validation_confidence(self, text: str, category: str, subcategories: List[str]) -> float:
        """Calculate confidence score for a given classification"""
        try:
            # Use keyword matching as a simple confidence measure
            keyword_scores = find_categories_by_keywords(text, threshold=1)
            category_score = keyword_scores.get(category, 0)
            
            # Simple confidence calculation
            max_score = max(keyword_scores.values()) if keyword_scores else 1
            confidence = category_score / max_score if max_score > 0 else 0.5
            
            return min(confidence, 1.0)
        except:
            return 0.5
    
    def get_category_suggestions(self, text: str, top_k: int = 3) -> List[str]:
        """Get category suggestions for a text"""
        try:
            result = self.ensemble_classify(text)
            suggestions = list(result['all_scores'].keys())[:top_k]
            return suggestions
        except:
            return ['General Curiosity & Learning', 'Emotional Support', 'Motivation & Self-Growth']

# Global classifier instance
text_classifier = TextClassifier()

def classify_text(text: str) -> Dict:
    """Simple interface for text classification"""
    return text_classifier.ensemble_classify(text)

def validate_classification_simple(text: str, category: str, subcategories: List[str]) -> bool:
    """Simple interface for classification validation"""
    result = text_classifier.validate_classification(text, category, subcategories)
    return result['is_valid']
