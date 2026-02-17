"""
Data loading utilities
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, Optional


class DataLoader:
    """Load and prepare data for model training"""
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
    
    def load_raw_data(self) -> pd.DataFrame:
        """
        Load raw data from Excel file
        
        Returns:
            DataFrame with raw data
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        df = pd.read_excel(self.data_path)
        return df
    
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare data for model training
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Prepared DataFrame
        """
        # Handle missing values
        df['likes'] = df['likes'].fillna(0)
        df['comments'] = df['comments'].fillna(0)
        df['shares'] = df['shares'].fillna(0)
        
        # Calculate total engagement
        df['total_engagement'] = df['likes'] + (df['comments'] * 2) + (df['shares'] * 3)
        
        # Categorize engagement
        df['engagement_score'] = df['total_engagement'].apply(self._categorize_engagement, args=(df,))
        
        return df
    
    @staticmethod
    def _categorize_engagement(score: float, df: pd.DataFrame) -> str:
        """Categorize engagement score into High/Medium/Low"""
        if score >= df['total_engagement'].quantile(0.67):
            return 'High'
        elif score >= df['total_engagement'].quantile(0.33):
            return 'Medium'
        else:
            return 'Low'
    
    def split_data(self, df: pd.DataFrame, test_size: float = 0.2, 
                   random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into train and test sets
        
        Args:
            df: DataFrame to split
            test_size: Proportion of test set
            random_state: Random seed
            
        Returns:
            Tuple of (train_df, test_df)
        """
        from sklearn.model_selection import train_test_split
        
        train_df, test_df = train_test_split(
            df, 
            test_size=test_size, 
            random_state=random_state,
            stratify=df['engagement_score']
        )
        
        return train_df, test_df
    
    def save_processed_data(self, df: pd.DataFrame, output_path: str):
        """
        Save processed data to CSV
        
        Args:
            df: DataFrame to save
            output_path: Path to save file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")
