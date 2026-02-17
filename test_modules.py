"""
Quick test script to verify all modules work correctly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append('src')

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from preprocessing import DataLoader, TextCleaner
        print("  ✓ preprocessing modules imported")
    except Exception as e:
        print(f"  ✗ preprocessing import failed: {e}")
        return False
    
    try:
        from features import TextFeatureExtractor, EngagementFeatureExtractor
        print("  ✓ features modules imported")
    except Exception as e:
        print(f"  ✗ features import failed: {e}")
        return False
    
    return True

def test_text_features():
    """Test text feature extraction"""
    print("\nTesting text feature extraction...")
    
    from features import TextFeatureExtractor
    
    extractor = TextFeatureExtractor()
    sample_text = """🚀 Just launched my new AI project!
    Built a machine learning model that predicts customer behavior.
    Check out the demo link in comments!
    #MachineLearning #AI #DataScience"""
    
    features = extractor.extract_features(sample_text)
    
    print(f"  ✓ Extracted {len(features)} features")
    print(f"  Sample features:")
    for key, value in list(features.items())[:5]:
        print(f"    - {key}: {value}")
    
    return True

def test_text_cleaner():
    """Test text cleaning"""
    print("\nTesting text cleaning...")
    
    from preprocessing import TextCleaner
    
    cleaner = TextCleaner()
    sample_text = "Check out https://example.com and follow @username! #AI"
    cleaned = cleaner.clean_text(sample_text)
    
    print(f"  Original: {sample_text}")
    print(f"  Cleaned: {cleaned}")
    print("  ✓ Text cleaning works")
    
    return True

def test_engagement_features():
    """Test engagement feature calculation"""
    print("\nTesting engagement features...")
    
    from features import EngagementFeatureExtractor
    
    extractor = EngagementFeatureExtractor()
    score = extractor.calculate_engagement_score(100, 10, 5)
    
    print(f"  Engagement score (100 likes, 10 comments, 5 shares): {score}")
    print("  ✓ Engagement calculation works")
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Module Testing Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_text_features,
        test_text_cleaner,
        test_engagement_features
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 60)

if __name__ == "__main__":
    main()
