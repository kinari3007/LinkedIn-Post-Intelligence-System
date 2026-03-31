"""
Flask API for LinkedIn Post Intelligence System
Provides endpoints for engagement prediction and feedback collection
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from features.text_features import TextFeatureExtractor

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Global variables for models
model = None
vectorizer = None
text_extractor = None

def load_models():
    """Load ML models at startup"""
    global model, vectorizer, text_extractor
    
    try:
        # Load SEMANTIC models (length-independent predictions)
        model_path = Path(__file__).parent.parent / 'src' / 'models' / 'semantic_engagement_model.pkl'
        vectorizer_path = Path(__file__).parent.parent / 'src' / 'models' / 'semantic_tfidf_vectorizer.pkl'
        
        print("Loading semantic models (length-independent)...")
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        text_extractor = TextFeatureExtractor()
        print("✓ Semantic models loaded successfully!")
        print("  → Predictions based on content quality, NOT text length")
        
    except Exception as e:
        print(f"✗ Error loading models: {e}")
        raise

@app.route('/', methods=['GET'])
def home():
    """API home endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'LinkedIn Post Intelligence API',
        'version': '1.0',
        'endpoints': {
            '/predict': 'POST - Predict engagement for a post',
            '/feedback': 'POST - Submit user feedback',
            '/health': 'GET - Check API health'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': model is not None and vectorizer is not None
    })

def analyze_lines_weighted(post_text, vectorizer, model):
    """
    Analyze each line independently and calculate quality scores
    Returns average quality score independent of text length
    """
    lines = [line.strip() for line in post_text.split('\n') if line.strip()]
    
    if not lines:
        return {'avg_score': 0, 'line_scores': [], 'quality_indicators': {}}
    
    line_scores = []
    quality_indicators = {
        'has_strong_opener': False,
        'has_call_to_action': False,
        'has_question': False,
        'has_hashtags': False,
        'has_emojis': False,
        'engagement_words': 0
    }
    
    # High-engagement keywords (length-independent)
    engagement_keywords = [
        'new', 'launch', 'excited', 'proud', 'share', 'learn', 'grow',
        'success', 'achieve', 'build', 'create', 'innovate', 'transform',
        'opportunity', 'experience', 'journey', 'milestone', 'breakthrough'
    ]
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        line_score = 0
        
        # Score based on content quality (not length)
        # 1. Strong opener (first line)
        if i == 0:
            if any(word in line_lower for word in ['🚀', '💡', '🎯', '✨', '🔥']):
                line_score += 15
                quality_indicators['has_strong_opener'] = True
            if any(word in line_lower for word in ['excited', 'proud', 'thrilled', 'happy']):
                line_score += 10
                quality_indicators['has_strong_opener'] = True
        
        # 2. Call-to-action indicators
        cta_phrases = ['check out', 'link in', 'comment below', 'share your', 'let me know', 
                       'what do you think', 'thoughts?', 'dm me', 'reach out']
        if any(phrase in line_lower for phrase in cta_phrases):
            line_score += 20
            quality_indicators['has_call_to_action'] = True
        
        # 3. Question engagement
        if '?' in line:
            line_score += 15
            quality_indicators['has_question'] = True
        
        # 4. Hashtags (quality over quantity)
        hashtag_count = line.count('#')
        if 1 <= hashtag_count <= 3:
            line_score += 10 * hashtag_count
            quality_indicators['has_hashtags'] = True
        elif hashtag_count > 3:
            line_score += 10  # Penalize too many hashtags
        
        # 5. Emojis (moderate use)
        emoji_count = sum(1 for char in line if ord(char) > 127)
        if 1 <= emoji_count <= 3:
            line_score += 5 * emoji_count
            quality_indicators['has_emojis'] = True
        
        # 6. Engagement keywords
        keyword_count = sum(1 for word in engagement_keywords if word in line_lower)
        if keyword_count > 0:
            line_score += 8 * keyword_count
            quality_indicators['engagement_words'] += keyword_count
        
        # 7. Exclamation marks (enthusiasm)
        exclamation_count = line.count('!')
        if 1 <= exclamation_count <= 2:
            line_score += 5 * exclamation_count
        
        # 8. Numbers and data (credibility)
        if any(char.isdigit() for char in line):
            line_score += 8
        
        # Normalize score per line (0-100 scale)
        line_score = min(line_score, 100)
        line_scores.append(line_score)
    
    # Calculate average quality (length-independent)
    avg_score = sum(line_scores) / len(line_scores) if line_scores else 0
    
    return {
        'avg_score': avg_score,
        'line_scores': line_scores,
        'quality_indicators': quality_indicators,
        'num_lines': len(lines)
    }

def adjust_prediction_by_quality(base_prediction, base_probabilities, line_scores, 
                                 text_features, classes):
    """
    Adjust prediction based on content quality rather than length
    """
    avg_quality = line_scores['avg_score']
    quality_indicators = line_scores['quality_indicators']
    
    # Calculate quality bonus (independent of length)
    quality_bonus = 0
    
    # Strong opener bonus
    if quality_indicators['has_strong_opener']:
        quality_bonus += 0.10
    
    # Engagement elements bonus
    if quality_indicators['has_call_to_action']:
        quality_bonus += 0.15
    
    if quality_indicators['has_question']:
        quality_bonus += 0.10
    
    # Hashtag bonus (if present and reasonable)
    if quality_indicators['has_hashtags'] and 1 <= text_features['hashtag_count'] <= 3:
        quality_bonus += 0.08
    
    # Emoji bonus (if moderate)
    if quality_indicators['has_emojis'] and 1 <= text_features['emoji_count'] <= 3:
        quality_bonus += 0.05
    
    # Engagement words bonus
    if quality_indicators['engagement_words'] >= 2:
        quality_bonus += 0.10
    
    # Convert quality score to probability adjustment
    # High quality (>60) boosts High engagement probability
    # Low quality (<30) boosts Low engagement probability
    
    adjusted_probs = base_probabilities.copy()
    
    if avg_quality >= 60:
        # High quality content - boost High engagement
        high_idx = list(classes).index('High')
        low_idx = list(classes).index('Low')
        
        # Shift probability from Low to High
        shift = min(quality_bonus, adjusted_probs[low_idx] * 0.5)
        adjusted_probs[high_idx] += shift
        adjusted_probs[low_idx] -= shift
        
    elif avg_quality <= 30:
        # Low quality content - boost Low engagement
        high_idx = list(classes).index('High')
        low_idx = list(classes).index('Low')
        
        # Shift probability from High to Low
        shift = min(quality_bonus, adjusted_probs[high_idx] * 0.5)
        adjusted_probs[low_idx] += shift
        adjusted_probs[high_idx] -= shift
    
    # Normalize probabilities
    adjusted_probs = adjusted_probs / adjusted_probs.sum()
    
    # Get new prediction
    adjusted_prediction = classes[np.argmax(adjusted_probs)]
    
    return adjusted_prediction, adjusted_probs

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict engagement level for a LinkedIn post
    
    Request JSON:
    {
        "user_id": "U001",
        "post_text": "Your LinkedIn post content here..."
    }
    
    Response JSON:
    {
        "engagement_level": "High|Medium|Low",
        "confidence": 89.5,
        "probabilities": {...},
        "key_factors": {...},
        "suggestions": [...]
    }
    """
    try:
        # Get request data
        data = request.json
        
        if not data or 'post_text' not in data:
            return jsonify({
                'error': 'Missing post_text in request'
            }), 400
        
        post_text = data.get('post_text', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        if not post_text:
            return jsonify({
                'error': 'Post text cannot be empty'
            }), 400
        
        # Extract text features
        text_features = text_extractor.extract_features(post_text)
        
        # NEW: Line-by-line weighted scoring (length-independent)
        line_scores = analyze_lines_weighted(post_text, vectorizer, model)
        
        # Vectorize text for model
        text_tfidf = vectorizer.transform([post_text])
        
        # Make base prediction
        base_prediction = model.predict(text_tfidf)[0]
        base_probabilities = model.predict_proba(text_tfidf)[0]
        
        # NEW: Adjust prediction based on line quality (not length)
        adjusted_prediction, adjusted_probabilities = adjust_prediction_by_quality(
            base_prediction, 
            base_probabilities, 
            line_scores,
            text_features,
            model.classes_
        )
        
        # Use adjusted prediction
        prediction = adjusted_prediction
        probabilities = adjusted_probabilities
        
        # Get class labels (High, Low, Medium)
        classes = model.classes_
        prob_dict = {
            classes[i]: round(float(probabilities[i]) * 100, 2) 
            for i in range(len(classes))
        }
        
        # Get confidence (max probability)
        confidence = round(float(max(probabilities)) * 100, 2)
        
        # Generate suggestions
        suggestions = generate_suggestions(prediction, text_features)
        
        # Get top contributing words
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = text_tfidf.toarray()[0]
        top_indices = np.argsort(tfidf_scores)[-10:][::-1]
        top_words = [feature_names[i] for i in top_indices if tfidf_scores[i] > 0]
        
        # Build response
        response = {
            'success': True,
            'user_id': user_id,
            'engagement_level': prediction,
            'confidence': confidence,
            'probabilities': prob_dict,
            'quality_analysis': {
                'overall_quality_score': round(line_scores['avg_score'], 2),
                'quality_rating': 'High' if line_scores['avg_score'] >= 60 else 'Medium' if line_scores['avg_score'] >= 30 else 'Low',
                'has_strong_opener': line_scores['quality_indicators']['has_strong_opener'],
                'has_call_to_action': line_scores['quality_indicators']['has_call_to_action'],
                'has_question': line_scores['quality_indicators']['has_question'],
                'engagement_words_count': line_scores['quality_indicators']['engagement_words']
            },
            'key_factors': {
                'text_length': text_features['text_length'],
                'word_count': text_features['word_count'],
                'line_count': text_features['line_count'],
                'hashtag_count': text_features['hashtag_count'],
                'emoji_count': text_features['emoji_count'],
                'has_cta': text_features['has_cta'],
                'has_question': text_features['has_question'],
                'exclamation_count': text_features['exclamation_count']
            },
            'top_words': top_words[:5],
            'suggestions': suggestions
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Store user feedback
    
    Request JSON:
    {
        "user_id": "U001",
        "post_text": "...",
        "predicted_level": "High",
        "helpful": true,
        "comment": "Optional comment"
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
        
        # In a production system, you would save this to a database
        # For now, we'll just log it
        user_id = data.get('user_id', 'anonymous')
        helpful = data.get('helpful', None)
        comment = data.get('comment', '')
        
        print(f"Feedback received from {user_id}: helpful={helpful}, comment={comment}")
        
        # TODO: Save to database or file
        # save_feedback_to_db(data)
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your feedback!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_suggestions(prediction, features):
    """
    Generate improvement suggestions based on content quality (not length)
    
    Args:
        prediction: Predicted engagement level (High/Medium/Low)
        features: Dictionary of text features
    
    Returns:
        List of suggestion strings
    """
    suggestions = []
    
    # Focus on quality over quantity
    # Only suggest length changes if extremely short or long
    if features['word_count'] < 10:
        suggestions.append("📝 Add a bit more context - even short posts benefit from 15-20 words")
    elif features['word_count'] > 150:
        suggestions.append("✂️ Consider breaking into multiple posts - very long posts may lose readers")
    
    # Hashtag suggestions (quality over quantity)
    if features['hashtag_count'] == 0:
        suggestions.append("🏷️ Add 2-3 relevant hashtags to increase discoverability")
    elif features['hashtag_count'] > 5:
        suggestions.append("⚠️ Too many hashtags can look spammy - stick to 2-3 most relevant ones")
    elif features['hashtag_count'] == 1:
        suggestions.append("🏷️ Consider adding 1-2 more relevant hashtags for better reach")
    
    # Emoji suggestions (moderate use)
    if features['emoji_count'] == 0:
        suggestions.append("😊 Add 1-2 emojis to make your post more engaging and eye-catching")
    
    # Call-to-action suggestions
    if not features['has_cta']:
        suggestions.append("💬 Include a call-to-action (e.g., 'What do you think?', 'Share your experience')")
    
    # Line break suggestions
    if features['line_count'] == 1 and features['word_count'] > 30:
        suggestions.append("📄 Break content into multiple lines for better readability")
    
    # Question suggestions
    if not features['has_question'] and prediction != 'High':
        suggestions.append("❓ Ask a question to encourage comments and engagement")
    
    # Exclamation suggestions
    if features['exclamation_count'] == 0 and prediction == 'Low':
        suggestions.append("❗ Add some enthusiasm with exclamation marks (but don't overdo it)")
    elif features['exclamation_count'] > 3:
        suggestions.append("⚠️ Too many exclamation marks - use them sparingly for impact")
    
    # If already high engagement predicted
    if prediction == 'High' and len(suggestions) == 0:
        suggestions.append("🎉 Great post! Your content is well-optimized for engagement")
    
    # Limit to top 5 suggestions
    return suggestions[:5]

# Load models when app starts
with app.app_context():
    load_models()

if __name__ == '__main__':
    print("=" * 60)
    print("LinkedIn Post Intelligence API")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("API Documentation: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
