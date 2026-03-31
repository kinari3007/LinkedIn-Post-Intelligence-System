"""
Configuration file for Flask API
"""

import os
from pathlib import Path

class Config:
    """Base configuration"""
    
    # Flask settings
    DEBUG = True
    TESTING = False
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Model paths
    BASE_DIR = Path(__file__).parent.parent
    MODEL_DIR = BASE_DIR / 'src' / 'models'
    MODEL_PATH = MODEL_DIR / 'engagement_model.pkl'
    VECTORIZER_PATH = MODEL_DIR / 'tfidf_vectorizer.pkl'
    
    # CORS settings
    CORS_ORIGINS = '*'  # In production, specify exact origins
    
    # API settings
    MAX_POST_LENGTH = 3000  # Maximum characters in a post
    MIN_POST_LENGTH = 5     # Minimum characters in a post
    
    # Rate limiting (for future implementation)
    RATE_LIMIT_ENABLED = False
    RATE_LIMIT_PER_MINUTE = 60
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'api.log'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    CORS_ORIGINS = ['https://yourdomain.com']  # Update with your domain
    RATE_LIMIT_ENABLED = True

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env='development'):
    """Get configuration based on environment"""
    return config.get(env, config['default'])
