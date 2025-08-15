import os
from datetime import datetime

class Config:
    """Configuration settings for Ledger of Legends"""
    
    # App settings
    APP_NAME = "Ledger of Legends"
    APP_VERSION = "2.0.0"
    APP_DESCRIPTION = "Intelligent financial analysis and insights for your ledger data"
    
    # File settings
    SUPPORTED_FORMATS = ['html', 'csv']
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Data processing settings
    DEFAULT_DATE_FORMAT = '%Y-%m-%d'
    CURRENCY_SYMBOL = '₹'
    CURRENCY_CODE = 'INR'
    
    # AI Analysis settings
    AI_CATEGORIES = {
        'Food & Dining': ['restaurant', 'food', 'meal', 'dining', 'cafe', 'pizza', 'burger', 'swiggy', 'zomato', 'dominos'],
        'Transportation': ['uber', 'ola', 'metro', 'bus', 'fuel', 'petrol', 'diesel', 'parking', 'toll', 'taxi', 'ride'],
        'Shopping': ['amazon', 'flipkart', 'myntra', 'shop', 'store', 'mall', 'clothing', 'electronics', 'online'],
        'Entertainment': ['movie', 'netflix', 'prime', 'hotstar', 'game', 'concert', 'theatre', 'cinema', 'streaming'],
        'Healthcare': ['medical', 'pharmacy', 'doctor', 'hospital', 'medicine', 'health', 'clinic', 'dental'],
        'Utilities': ['electricity', 'water', 'gas', 'internet', 'mobile', 'recharge', 'bill', 'utility'],
        'Education': ['course', 'book', 'tuition', 'college', 'university', 'education', 'training', 'learning'],
        'Investment': ['mutual', 'fund', 'stock', 'investment', 'sip', 'equity', 'portfolio', 'trading'],
        'Travel': ['hotel', 'flight', 'booking', 'travel', 'vacation', 'trip', 'airline', 'accommodation'],
        'Personal Care': ['salon', 'spa', 'beauty', 'gym', 'fitness', 'wellness', 'cosmetics', 'personal']
    }
    
    # Budget settings
    DEFAULT_MONTHLY_BUDGET = 50000
    BUDGET_WARNING_THRESHOLD = 0.8  # 80%
    BUDGET_CAUTION_THRESHOLD = 0.6  # 60%
    
    # Visualization settings
    CHART_COLORS = {
        'primary': '#667eea',
        'secondary': '#764ba2',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8'
    }
    
    # Filter settings
    DEFAULT_DATE_RANGE_DAYS = 365
    AMOUNT_RANGE_STEP = 100.0
    
    # Export settings
    EXPORT_FORMATS = ['csv', 'json', 'excel']
    DEFAULT_EXPORT_FORMAT = 'csv'
    
    # Performance settings
    CACHE_TTL = 3600  # 1 hour
    MAX_ROWS_DISPLAY = 1000
    
    # Notification settings
    ENABLE_NOTIFICATIONS = True
    NOTIFICATION_TYPES = ['budget_alert', 'anomaly_detection', 'spending_trend']
    
    @classmethod
    def get_environment_config(cls):
        """Get configuration from environment variables"""
        return {
            'debug': os.getenv('DEBUG', 'False').lower() == 'true',
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'max_file_size': int(os.getenv('MAX_FILE_SIZE', cls.MAX_FILE_SIZE)),
            'cache_ttl': int(os.getenv('CACHE_TTL', cls.CACHE_TTL))
        }
    
    @classmethod
    def get_user_preferences(cls):
        """Get default user preferences"""
        return {
            'currency_symbol': cls.CURRENCY_SYMBOL,
            'date_format': cls.DEFAULT_DATE_FORMAT,
            'monthly_budget': cls.DEFAULT_MONTHLY_BUDGET,
            'chart_theme': 'plotly_white',
            'language': 'en'
        }
