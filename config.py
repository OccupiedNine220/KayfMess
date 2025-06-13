import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'каЙфМесС_СеКрЕтНыЙ_КлЮч_B_3_4аСа_Н04и'
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # MongoDB
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/kayfmess'
    MONGODB_DB = 'kayfmess'
    
    # App Settings
    DEBUG = False
    TESTING = False
    SERVER_NAME = os.environ.get('SERVER_NAME') or 'kayfmess.qndk.fun'
    
    # Security
    SSL_REDIRECT = False
    
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')


class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = None


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SERVER_NAME = None
    MONGODB_DB = 'kayfmess_test'


class ProductionConfig(Config):
    # Security
    SSL_REDIRECT = True


class DockerConfig(ProductionConfig):
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://mongodb:27017/kayfmess'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
} 