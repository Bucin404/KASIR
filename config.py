import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        # Only use default in development
        import sys
        if 'pytest' not in sys.modules and os.environ.get('FLASK_ENV') == 'production':
            raise ValueError("SECRET_KEY must be set in production environment")
        SECRET_KEY = 'dev-secret-key-change-in-production'
    
    # Database Configuration
    # Priority: DATABASE_URL > MySQL individual params > SQLite default
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if not DATABASE_URL:
        # Try to build MySQL URL from individual parameters
        mysql_host = os.environ.get('MYSQL_HOST')
        mysql_port = os.environ.get('MYSQL_PORT', '3306')
        mysql_user = os.environ.get('MYSQL_USER')
        mysql_password = os.environ.get('MYSQL_PASSWORD')
        mysql_database = os.environ.get('MYSQL_DATABASE')
        
        if all([mysql_host, mysql_user, mysql_password, mysql_database]):
            DATABASE_URL = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}'
        else:
            # Fallback to SQLite for development
            DATABASE_URL = 'sqlite:///kasir.db'
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Enable connection health checks
        'pool_recycle': 3600,   # Recycle connections after 1 hour
    }
    
    # Midtrans Configuration (Sandbox)
    MIDTRANS_SERVER_KEY = os.environ.get('MIDTRANS_SERVER_KEY') or 'SB-Mid-server-YOUR_SERVER_KEY'
    MIDTRANS_CLIENT_KEY = os.environ.get('MIDTRANS_CLIENT_KEY') or 'SB-Mid-client-YOUR_CLIENT_KEY'
    MIDTRANS_IS_PRODUCTION = os.environ.get('MIDTRANS_IS_PRODUCTION', 'False').lower() == 'true'
    
    # Application Settings
    APP_NAME = 'KASIR Modern'
    APP_VERSION = '2.0.0'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Tax Configuration
    TAX_RATE = float(os.environ.get('TAX_RATE', '0.10'))  # Default 10% tax
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Upload Configuration
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_kasir.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
