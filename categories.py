"""
Category definitions and mapping for AI Baba advice system
"""
from typing import Dict, List, Set
import re

# Complete category structure as defined in requirements
CATEGORIES_STRUCTURE = {
    "Emotional Support": {
        "subcategories": [
            "Sadness / Depression",
            "Anxiety / Stress / Overthinking", 
            "Loneliness / Isolation",
            "Anger / Frustration",
            "Self-Doubt / Insecurity",
            "Fear (exam fear, failure fear, future fear)"
        ],
        "keywords": [
            "sad", "depression", "depressed", "lonely", "alone", "anxious", "stress", 
            "worried", "overthinking", "angry", "frustrated", "insecure", "doubt",
            "fear", "scared", "afraid", "nervous", "panic", "helpless", "hopeless"
        ]
    },
    
    "Motivation & Self-Growth": {
        "subcategories": [
            "Demotivation / Laziness",
            "Building Discipline & Consistency",
            "Time Management & Productivity",
            "Focus & Concentration", 
            "Learning New Skills / Knowledge",
            "Self-Confidence & Courage",
            "Handling Criticism"
        ],
        "keywords": [
            "motivation", "lazy", "procrastination", "discipline", "consistency", 
            "productivity", "focus", "concentration", "learning", "skills", 
            "confidence", "courage", "criticism", "growth", "improvement"
        ]
    },
    
    "Failures & Mistakes": {
        "subcategories": [
            "Academic Failure (exam, grades)",
            "Career / Job Failure", 
            "Business / Startup Failure",
            "Regret about Past Mistakes",
            "Learning from Mistakes",
            "Fear of Trying Again"
        ],
        "keywords": [
            "failure", "failed", "mistake", "regret", "exam", "grades", "career",
            "job", "business", "startup", "trying again", "second chance"
        ]
    },
    
    "Decision Making & Life Choices": {
        "subcategories": [
            "Career Choices (job vs higher studies)",
            "Relationship Choices",
            "Risk Taking vs Playing Safe", 
            "Confusion / Indecisiveness",
            "Choosing Priorities in Life"
        ],
        "keywords": [
            "decision", "choice", "choose", "confused", "indecisive", "career", 
            "relationship", "risk", "safe", "priorities", "dilemma"
        ]
    },
    
    "Relationships & Social Life": {
        "subcategories": [
            "Family Conflicts (parents, siblings)",
            "Friendship Issues",
            "Breakups / Love Failure",
            "Marriage / Partnership Problems", 
            "Trust Issues / Betrayal",
            "Social Anxiety / Fear of People"
        ],
        "keywords": [
            "family", "parents", "siblings", "friends", "friendship", "breakup",
            "love", "relationship", "marriage", "partner", "trust", "betrayal",
            "social", "people", "introvert"
        ]
    },
    
    "Career & Studies": {
        "subcategories": [
            "Exam Preparation Stress",
            "Study Techniques & Focus",
            "Choosing Career Path (engineering, medical, arts, etc.)",
            "Job Search Stress",
            "Workplace Pressure / Toxic Work Environment", 
            "Balancing Work & Life"
        ],
        "keywords": [
            "exam", "study", "studying", "career", "job", "work", "workplace",
            "engineering", "medical", "arts", "pressure", "toxic", "balance"
        ]
    },
    
    "Health & Lifestyle": {
        "subcategories": [
            "Physical Health Issues",
            "Mental Health Awareness", 
            "Fitness & Exercise Motivation",
            "Sleep Problems",
            "Addiction (phone, social media, smoking, alcohol, etc.)"
        ],
        "keywords": [
            "health", "fitness", "exercise", "sleep", "addiction", "phone",
            "social media", "smoking", "alcohol", "mental health", "physical"
        ]
    },
    
    "Money & Finance": {
        "subcategories": [
            "Financial Stress",
            "Saving & Budgeting",
            "Bad Financial Decisions", 
            "Greed / Over-Spending",
            "Career Growth for Better Earnings"
        ],
        "keywords": [
            "money", "financial", "finance", "saving", "budget", "spending",
            "earnings", "salary", "income", "debt", "investment"
        ]
    },
    
    "Spiritual / Philosophical": {
        "subcategories": [
            "Meaning of Life",
            "Patience & Acceptance",
            "Gratitude & Humility", 
            "Inner Peace & Meditation",
            "Karma & Destiny",
            "Hope & Faith in Future"
        ],
        "keywords": [
            "spiritual", "meaning", "life", "patience", "acceptance", "gratitude",
            "meditation", "karma", "destiny", "hope", "faith", "peace", "philosophy"
        ]
    },
    
    "General Curiosity & Learning": {
        "subcategories": [
            "Wanting to Learn Something New",
            "Curiosity about World / People",
            "Life Advice (general guidance)", 
            "Improving Communication Skills",
            "Developing Hobbies & Creativity"
        ],
        "keywords": [
            "learn", "learning", "curiosity", "curious", "advice", "guidance",
            "communication", "skills", "hobbies", "creativity", "knowledge"
        ]
    },
    
    "Smoking & Drinking Habits": {
        "subcategories": [
            "Health Impact",
            "Mental Health & Stress",
            "Addiction & Self-Control", 
            "Alternative Solutions"
        ],
        "keywords": [
            "smoking", "cigarette", "tobacco", "drinking", "alcohol", "beer",
            "wine", "addiction", "quit", "health impact", "lungs", "liver"
        ]
    },
    
    "Masturbation & Sexual Health": {
        "subcategories": [
            "Physical Health Myths & Facts",
            "Mental & Emotional Effects",
            "Self-Control & Balance", 
            "Spiritual Perspective"
        ],
        "keywords": [
            "masturbation", "sexual", "sex", "urges", "control", "guilt",
            "brahmacharya", "energy", "spiritual", "myths", "facts"
        ]
    }
}

def get_all_categories() -> List[str]:
    """Get list of all main categories"""
    return list(CATEGORIES_STRUCTURE.keys())

def get_all_subcategories(category: str = None) -> List[str]:
    """Get list of all subcategories, optionally filtered by main category"""
    if category and category in CATEGORIES_STRUCTURE:
        return CATEGORIES_STRUCTURE[category]["subcategories"]
    
    subcategories = []
    for cat_data in CATEGORIES_STRUCTURE.values():
        subcategories.extend(cat_data["subcategories"])
    return subcategories

def get_category_keywords(category: str) -> List[str]:
    """Get keywords for a specific category"""
    if category in CATEGORIES_STRUCTURE:
        return CATEGORIES_STRUCTURE[category]["keywords"]
    return []

def get_all_keywords() -> Dict[str, List[str]]:
    """Get all keywords mapped to their categories"""
    keyword_map = {}
    for category, data in CATEGORIES_STRUCTURE.items():
        keyword_map[category] = data["keywords"]
    return keyword_map

def find_categories_by_keywords(text: str, threshold: int = 1) -> Dict[str, int]:
    """
    Find potential categories based on keyword matching
    
    Args:
        text: Input text to analyze
        threshold: Minimum keyword matches required
        
    Returns:
        Dictionary of categories with their keyword match counts
    """
    text_lower = text.lower()
    category_scores = {}
    
    for category, data in CATEGORIES_STRUCTURE.items():
        keyword_count = 0
        for keyword in data["keywords"]:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, text_lower):
                keyword_count += 1
        
        if keyword_count >= threshold:
            category_scores[category] = keyword_count
    
    # Sort by score (descending)
    return dict(sorted(category_scores.items(), key=lambda x: x[1], reverse=True))

def validate_category_assignment(category: str, subcategories: List[str]) -> bool:
    """
    Validate if subcategories belong to the assigned category
    
    Args:
        category: Main category name
        subcategories: List of assigned subcategories
        
    Returns:
        True if all subcategories are valid for the category
    """
    if category not in CATEGORIES_STRUCTURE:
        return False
    
    valid_subcategories = set(CATEGORIES_STRUCTURE[category]["subcategories"])
    assigned_subcategories = set(subcategories)
    
    return assigned_subcategories.issubset(valid_subcategories)

def get_category_for_subcategory(subcategory: str) -> str:
    """
    Find which main category a subcategory belongs to
    
    Args:
        subcategory: Subcategory name
        
    Returns:
        Main category name or empty string if not found
    """
    for category, data in CATEGORIES_STRUCTURE.items():
        if subcategory in data["subcategories"]:
            return category
    return ""

def format_subcategories_string(subcategories: List[str]) -> str:
    """
    Format subcategories as comma-separated string for database storage
    
    Args:
        subcategories: List of subcategory names
        
    Returns:
        Comma-separated string
    """
    return ",".join(subcategories)

def parse_subcategories_string(subcategories_str: str) -> List[str]:
    """
    Parse comma-separated subcategories string from database
    
    Args:
        subcategories_str: Comma-separated subcategories string
        
    Returns:
        List of subcategory names
    """
    if not subcategories_str:
        return []
    return [sub.strip() for sub in subcategories_str.split(",") if sub.strip()]

# Category-specific prompt templates for better classification
CATEGORY_PROMPTS = {
    "Emotional Support": "This text seems to be about emotional distress, mental health struggles, feelings of sadness, anxiety, loneliness, anger, or fear.",
    "Motivation & Self-Growth": "This text appears to be about motivation, self-improvement, building habits, productivity, learning, or personal development.",
    "Failures & Mistakes": "This text relates to failures, mistakes, regrets, academic/career setbacks, or learning from past experiences.",
    "Decision Making & Life Choices": "This text involves decision making, life choices, career decisions, relationship choices, or feeling confused about options.",
    "Relationships & Social Life": "This text is about relationships, family conflicts, friendship issues, love problems, social anxiety, or interpersonal challenges.",
    "Career & Studies": "This text relates to career, studies, exams, job search, workplace issues, or educational concerns.",
    "Health & Lifestyle": "This text is about physical health, mental wellness, fitness, sleep, addictions, or lifestyle choices.",
    "Money & Finance": "This text deals with financial matters, money problems, budgeting, earnings, or financial decisions.",
    "Spiritual / Philosophical": "This text has spiritual or philosophical content about life's meaning, meditation, karma, faith, or inner peace.",
    "General Curiosity & Learning": "This text shows curiosity, desire to learn, seeking general advice, or developing new skills.",
    "Smoking & Drinking Habits": "This text specifically mentions smoking, drinking alcohol, or related health and addiction concerns.",
    "Masturbation & Sexual Health": "This text deals with sexual health, masturbation, related myths, emotional effects, or spiritual perspectives."
}
