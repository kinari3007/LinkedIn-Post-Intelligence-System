"""
Data processing pipeline
Run this script to process raw data and save to processed folder
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from preprocessing.data_loader import DataLoader
from preprocessing.text_cleaner import TextCleaner
from features.text_features import TextFeatureExtractor
from features.engagement_features import EngagementFeatureExtractor


def main():
    """Main data processing pipeline"""
    
    print("=" * 60)
    print("LinkedIn Post Intelligence - Data Processing Pipeline")
    print("=" * 60)
    
    # Initialize components
    data_loader = DataLoader('data/raw/LinkedIN_Caption_DataSet.xlsx')
    text_cleaner = TextCleaner(lowercase=False, remove_urls=False, remove_mentions=False)
    text_feature_extractor = TextFeatureExtractor()
    engagement_feature_extractor = EngagementFeatureExtractor()
    
    # Step 1: Load raw data
    print("\n[1/5] Loading raw data...")
    df = data_loader.load_raw_data()
    print(f"   ✓ Loaded {len(df)} records")
    
    # Step 2: Prepare data (handle missing values, calculate engagement)
    print("\n[2/5] Preparing data...")
    df = data_loader.prepare_data(df)
    print(f"   ✓ Engagement scores calculated")
    print(f"   ✓ Distribution: {df['engagement_score'].value_counts().to_dict()}")
    
    # Step 3: Extract text features
    print("\n[3/5] Extracting text features...")
    text_features = text_feature_extractor.extract_batch_features(df['post_text'].tolist())
    df = df.join(text_features)
    print(f"   ✓ Extracted {len(text_features.columns)} text features")
    
    # Step 4: Extract engagement features
    print("\n[4/5] Extracting engagement features...")
    df = engagement_feature_extractor.extract_engagement_features(df)
    print(f"   ✓ Engagement features calculated")
    
    # Step 5: Save processed data
    print("\n[5/5] Saving processed data...")
    
    # Save full processed dataset
    data_loader.save_processed_data(df, 'data/processed/processed_data.csv')
    
    # Split and save train/test sets
    train_df, test_df = data_loader.split_data(df)
    data_loader.save_processed_data(train_df, 'data/processed/train_data.csv')
    data_loader.save_processed_data(test_df, 'data/processed/test_data.csv')
    
    print(f"   ✓ Full dataset: {len(df)} records")
    print(f"   ✓ Training set: {len(train_df)} records")
    print(f"   ✓ Test set: {len(test_df)} records")
    
    # Display summary statistics
    print("\n" + "=" * 60)
    print("Processing Complete!")
    print("=" * 60)
    print("\nDataset Summary:")
    print(f"  Total Records: {len(df)}")
    print(f"  Features: {len(df.columns)}")
    print(f"\nEngagement Distribution:")
    for category, count in df['engagement_score'].value_counts().items():
        percentage = (count / len(df)) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")
    
    print("\nFiles saved to:")
    print("  - data/processed/processed_data.csv")
    print("  - data/processed/train_data.csv")
    print("  - data/processed/test_data.csv")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
