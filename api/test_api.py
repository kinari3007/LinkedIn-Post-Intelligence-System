"""
Test script for LinkedIn Post Intelligence API
Run this after starting the Flask server to verify everything works
"""

import requests
import json

API_URL = 'http://localhost:5000'

def test_home():
    """Test home endpoint"""
    print("\n" + "="*60)
    print("Testing Home Endpoint")
    print("="*60)
    
    response = requests.get(f'{API_URL}/')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    response = requests.get(f'{API_URL}/health')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def test_predict_high_engagement():
    """Test prediction with high engagement post"""
    print("\n" + "="*60)
    print("Testing Prediction - High Engagement Post")
    print("="*60)
    
    post_text = """🚀 Excited to share my latest AI project!

Built a machine learning model that predicts customer behavior with 95% accuracy.
This could revolutionize how businesses understand their customers.

Key features:
✅ Real-time predictions
✅ Easy integration
✅ Scalable architecture

What challenges have you faced with customer analytics? Let's discuss! 💬

#AI #MachineLearning #DataScience #Innovation #TechLeadership"""
    
    payload = {
        'user_id': 'test_user_1',
        'post_text': post_text
    }
    
    response = requests.post(f'{API_URL}/predict', json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nEngagement Level: {result['engagement_level']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"\nProbabilities:")
        for level, prob in result['probabilities'].items():
            print(f"  {level}: {prob}%")
        print(f"\nKey Factors:")
        for key, value in result['key_factors'].items():
            print(f"  {key}: {value}")
        print(f"\nTop Words: {', '.join(result['top_words'])}")
        print(f"\nSuggestions:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")
    else:
        print(f"Error: {response.json()}")
    
    return response.status_code == 200

def test_predict_low_engagement():
    """Test prediction with low engagement post"""
    print("\n" + "="*60)
    print("Testing Prediction - Low Engagement Post")
    print("="*60)
    
    post_text = "Just finished a project."
    
    payload = {
        'user_id': 'test_user_2',
        'post_text': post_text
    }
    
    response = requests.post(f'{API_URL}/predict', json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nEngagement Level: {result['engagement_level']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"\nSuggestions:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")
    else:
        print(f"Error: {response.json()}")
    
    return response.status_code == 200

def test_predict_medium_engagement():
    """Test prediction with medium engagement post"""
    print("\n" + "="*60)
    print("Testing Prediction - Medium Engagement Post")
    print("="*60)
    
    post_text = """Working on a new data analysis project. 
Learning a lot about Python and pandas. 
#DataScience #Python"""
    
    payload = {
        'user_id': 'test_user_3',
        'post_text': post_text
    }
    
    response = requests.post(f'{API_URL}/predict', json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nEngagement Level: {result['engagement_level']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"\nSuggestions:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")
    else:
        print(f"Error: {response.json()}")
    
    return response.status_code == 200

def test_feedback():
    """Test feedback endpoint"""
    print("\n" + "="*60)
    print("Testing Feedback Endpoint")
    print("="*60)
    
    payload = {
        'user_id': 'test_user_1',
        'post_text': 'Test post',
        'predicted_level': 'High',
        'helpful': True,
        'comment': 'Very accurate prediction!'
    }
    
    response = requests.post(f'{API_URL}/feedback', json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def test_error_handling():
    """Test error handling with invalid input"""
    print("\n" + "="*60)
    print("Testing Error Handling")
    print("="*60)
    
    # Test with empty post text
    payload = {
        'user_id': 'test_user',
        'post_text': ''
    }
    
    response = requests.post(f'{API_URL}/predict', json=payload)
    print(f"Empty text - Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test with missing post_text
    payload = {
        'user_id': 'test_user'
    }
    
    response = requests.post(f'{API_URL}/predict', json=payload)
    print(f"\nMissing text - Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return True

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("LinkedIn Post Intelligence API - Test Suite")
    print("="*60)
    print("Make sure the Flask server is running on http://localhost:5000")
    print("="*60)
    
    tests = [
        ("Home Endpoint", test_home),
        ("Health Check", test_health),
        ("High Engagement Prediction", test_predict_high_engagement),
        ("Low Engagement Prediction", test_predict_low_engagement),
        ("Medium Engagement Prediction", test_predict_medium_engagement),
        ("Feedback Submission", test_feedback),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except requests.exceptions.ConnectionError:
            print(f"\n❌ ERROR: Cannot connect to API at {API_URL}")
            print("Make sure the Flask server is running:")
            print("  cd api")
            print("  python app.py")
            return
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check the output above for details.")

if __name__ == '__main__':
    run_all_tests()
