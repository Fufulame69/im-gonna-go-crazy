import os
import sys
from dotenv import load_dotenv
from enum import Enum
from typing import Optional

# Load environment variables from .env file
# Check if we're running in a PyInstaller bundle
if getattr(sys, 'frozen', False):
    # We're running in a PyInstaller bundle
    bundle_dir = sys._MEIPASS
    env_path = os.path.join(bundle_dir, '.env')
else:
    # We're running in a normal Python environment
    env_path = '.env'

load_dotenv(env_path)

class DatabaseType(Enum):
    """Enum for supported database types"""
    LOCAL = "local"
    FIREBASE = "firebase"

class DatabaseConfig:
    """Centralized database configuration management"""
    
    def __init__(self):
        # Get database type from environment, default to Firebase
        db_type = os.getenv("DATABASE_TYPE", "firebase").lower()
        
        try:
            self.database_type = DatabaseType(db_type)
        except ValueError:
            print(f"Warning: Invalid DATABASE_TYPE '{db_type}'. Defaulting to Firebase.")
            self.database_type = DatabaseType.FIREBASE
        
        # Firebase configuration
        self.firebase_database_url = os.getenv("FIREBASE_DATABASE_URL")
        self.firebase_service_account_key = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
        
        # Local database configuration
        self.local_db_path = os.getenv("LOCAL_DB_PATH", "source/database/database.json")
        
        # Validate configuration
        self._validate_configuration()
    
    def _validate_configuration(self):
        """Validate the current configuration"""
        if self.database_type == DatabaseType.FIREBASE:
            if not self.firebase_database_url:
                raise ValueError("FIREBASE_DATABASE_URL is required when using Firebase")
            if not self.firebase_service_account_key:
                raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY is required when using Firebase")
        
        elif self.database_type == DatabaseType.LOCAL:
            # Ensure the directory for local database exists
            db_dir = os.path.dirname(self.local_db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
    
    def is_using_firebase(self) -> bool:
        """Check if Firebase is configured as the database"""
        return self.database_type == DatabaseType.FIREBASE
    
    def is_using_local(self) -> bool:
        """Check if local database is configured"""
        return self.database_type == DatabaseType.LOCAL
    
    def get_firebase_config(self) -> dict:
        """Get Firebase configuration as a dictionary"""
        if not self.is_using_firebase():
            raise ValueError("Firebase is not configured as the database type")
        
        return {
            "databaseURL": self.firebase_database_url,
            "serviceAccountKey": self.firebase_service_account_key
        }
    
    def get_local_db_path(self) -> str:
        """Get the local database file path"""
        if not self.is_using_local():
            raise ValueError("Local database is not configured as the database type")
        
        return self.local_db_path
    
    def switch_to_firebase(self):
        """Switch database configuration to Firebase"""
        self.database_type = DatabaseType.FIREBASE
        self._validate_configuration()
        print("Switched to Firebase database")
    
    def switch_to_local(self):
        """Switch database configuration to local"""
        self.database_type = DatabaseType.LOCAL
        self._validate_configuration()
        print("Switched to local database")

# Create a global configuration instance
db_config = DatabaseConfig()

# Backward compatibility - keep the old variable names for existing code
USING_LOCAL_DB = db_config.is_using_local()
USING_FIREBASE_REALTIME_DB = db_config.is_using_firebase()
FIREBASE_DATABASE_URL = db_config.firebase_database_url
FIREBASE_SERVICE_ACCOUNT_KEY = db_config.firebase_service_account_key

# Application configuration
APP_NAME = "Waldorf Access Form Generator"
APP_VERSION = "1.0.0"

# GUI Configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Theme Configuration
THEME = {
    "primary_color": "#2c3e50",
    "secondary_color": "#3498db",
    "accent_color": "#e74c3c",
    "background_color": "#ecf0f1",
    "text_color": "#2c3e50",
    "font_family": "Arial",
    "font_size": 10
}