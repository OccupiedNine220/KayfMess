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
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'postfix'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'kayfmess@qndk.fun'
    MAIL_MAX_EMAILS = os.environ.get('MAIL_MAX_EMAILS') or 100
    MAIL_SUPPRESS_SEND = os.environ.get('MAIL_SUPPRESS_SEND', 'false').lower() == 'true'
    MAIL_ASCII_ATTACHMENTS = os.environ.get('MAIL_ASCII_ATTACHMENTS', 'false').lower() == 'true'


class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = None
    MAIL_SUPPRESS_SEND = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SERVER_NAME = None
    MONGODB_DB = 'kayfmess_test'
    MAIL_SUPPRESS_SEND = True


class ProductionConfig(Config):
    # Security
    SSL_REDIRECT = True


class DockerConfig(ProductionConfig):
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://mongodb:27017/kayfmess'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'postfix'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
} 