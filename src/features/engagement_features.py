"""
Engagement-based feature extraction
"""

import pandas as pd
import numpy as np
from typing import Dict


class EngagementFeatureExtractor:
    """Extract features related to engagement metrics"""
    
    def __init__(self):
        self.weights = {
            'likes': 1,
            'comments': 2,
            'shares': 3
        }
    
    def calculate_engagement_score(self, likes: float, comments: float, shares: float) -> float:
        """
        Calculate weighted engagement score
        
        Args:
            likes: Number of likes
            comments: Number of comments
            shares: Number of shares
            
        Returns:
            Weighted engagement score
        """
        return (likes * self.weights['likes'] + 
                comments * self.weights['comments'] + 
                shares * self.weights['shares'])
    
    def categorize_engagement(self, score: float, quantiles: Dict[str, float]) -> str:
        """
        Categorize engagement score into High/Medium/Low
        
        Args:
            score: Engagement score
            quantiles: Dictionary with 'high' and 'medium' thresholds
            
        Returns:
            Category string
        """
        if score >= quantiles['high']:
            return 'High'
        elif score >= quantiles['medium']:
            return 'Medium'
        else:
            return 'Low'
    
    def extract_engagement_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract engagement-related features
        
        Args:
            df: DataFrame with engagement metrics
            
        Returns:
            DataFrame with additional features
        """
        df = df.copy()
        
        # Calculate total engagement
        df['total_engagement'] = df.apply(
            lambda row: self.calculate_engagement_score(
                row['likes'], row['comments'], row['shares']
            ), axis=1
        )
        
        # Calculate engagement ratios
        df['comment_like_ratio'] = df['comments'] / (df['likes'] + 1)
        df['share_like_ratio'] = df['shares'] / (df['likes'] + 1)
        df['share_comment_ratio'] = df['shares'] / (df['comments'] + 1)
        
        # Calculate engagement rate (if total possible engagement is known)
        # For now, we'll use relative metrics
        df['engagement_intensity'] = (df['comments'] + df['shares']) / (df['likes'] + 1)
        
        return df
    
    def get_quantiles(self, df: pd.DataFrame, column: str = 'total_engagement') -> Dict[str, float]:
        """
        Get quantile thresholds for categorization
        
        Args:
            df: DataFrame with engagement data
            column: Column name to calculate quantiles
            
        Returns:
            Dictionary with quantile thresholds
        """
        return {
            'high': df[column].quantile(0.67),
            'medium': df[column].quantile(0.33)
        }
