"""
Text cleaning and preprocessing utilities
"""

import re
import string
from typing import List


class TextCleaner:
    """Clean and preprocess text data for model training"""
    
    def __init__(self, lowercase=True, remove_urls=True, remove_mentions=True):
        self.lowercase = lowercase
        self.remove_urls = remove_urls
        self.remove_mentions = remove_mentions
    
    def clean_text(self, text: str) -> str:
        """
        Clean a single text string
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text string
        """
        if not isinstance(text, str):
            return ""
        
        # Remove URLs
        if self.remove_urls:
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove mentions (@username)
        if self.remove_mentions:
            text = re.sub(r'@\w+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Convert to lowercase
        if self.lowercase:
            text = text.lower()
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def clean_batch(self, texts: List[str]) -> List[str]:
        """
        Clean a batch of text strings
        
        Args:
            texts: List of raw text strings
            
        Returns:
            List of cleaned text strings
        """
        return [self.clean_text(text) for text in texts]
    
    def remove_emojis(self, text: str) -> str:
        """Remove emojis from text"""
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)
    
    def extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        return re.findall(r'#\w+', text)
    
    def count_hashtags(self, text: str) -> int:
        """Count number of hashtags in text"""
        return len(self.extract_hashtags(text))
