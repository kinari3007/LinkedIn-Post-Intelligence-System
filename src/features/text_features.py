"""
Text feature extraction utilities
"""

import re
import pandas as pd
from typing import Dict, List


class TextFeatureExtractor:
    """Extract features from text data"""
    
    def __init__(self):
        self.cta_keywords = [
            'click', 'link', 'check out', 'read more', 'learn more',
            'visit', 'download', 'register', 'sign up', 'join',
            'comment', 'share', 'like', 'follow', 'subscribe'
        ]
        
        self.question_words = ['what', 'why', 'how', 'when', 'where', 'who', 'which']
    
    def extract_features(self, text: str) -> Dict[str, float]:
        """
        Extract all text features from a single text
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary of features
        """
        features = {}
        
        # Basic text statistics
        features['text_length'] = len(text)
        features['word_count'] = len(text.split())
        features['line_count'] = text.count('\n') + 1
        features['avg_word_length'] = self._avg_word_length(text)
        
        # Punctuation features
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['emoji_count'] = self._count_emojis(text)
        
        # Hashtag features
        features['hashtag_count'] = len(re.findall(r'#\w+', text))
        
        # URL features
        features['url_count'] = len(re.findall(r'http\S+|www\S+', text))
        
        # Mention features
        features['mention_count'] = len(re.findall(r'@\w+', text))
        
        # Call-to-action features
        features['has_cta'] = int(self._has_call_to_action(text))
        
        # Question features
        features['has_question'] = int(self._has_question(text))
        
        # Capitalization features
        features['uppercase_ratio'] = self._uppercase_ratio(text)
        
        return features
    
    def extract_batch_features(self, texts: List[str]) -> pd.DataFrame:
        """
        Extract features from a batch of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            DataFrame with features
        """
        features_list = [self.extract_features(text) for text in texts]
        return pd.DataFrame(features_list)
    
    def _avg_word_length(self, text: str) -> float:
        """Calculate average word length"""
        words = text.split()
        if not words:
            return 0
        return sum(len(word) for word in words) / len(words)
    
    def _count_emojis(self, text: str) -> int:
        """Count emojis in text"""
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        return len(emoji_pattern.findall(text))
    
    def _has_call_to_action(self, text: str) -> bool:
        """Check if text contains call-to-action"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.cta_keywords)
    
    def _has_question(self, text: str) -> bool:
        """Check if text contains a question"""
        if '?' in text:
            return True
        text_lower = text.lower()
        return any(text_lower.startswith(word) for word in self.question_words)
    
    def _uppercase_ratio(self, text: str) -> float:
        """Calculate ratio of uppercase letters"""
        if not text:
            return 0
        uppercase_count = sum(1 for c in text if c.isupper())
        return uppercase_count / len(text)
