import os
import sys
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import config

class DatabaseManager:
    def __init__(self):
        self.firebase_app = None
        self.firebase_initialized = False
        
        # Initialize Firebase if needed
        if config.db_config.is_using_firebase():
            self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase connection with service account credentials"""
        try:
            if not self.firebase_initialized:
                # Check if Firebase is already initialized
                try:
                    app = firebase_admin.get_app('waldorf_db')
                    if app:
                        self.firebase_app = app
                        self.firebase_initialized = True
                        print("Firebase already initialized")
                        return
                except ValueError:
                    pass  # App not initialized, continue with initialization
                
                # Initialize Firebase with service account credentials
                try:
                    firebase_config = config.db_config.get_firebase_config()
                    
                    # Get the path to the service account key
                    service_account_path = firebase_config["serviceAccountKey"]
                    # If path is relative, make it relative to project root
                    if not os.path.isabs(service_account_path):
                        # Check if we're running in a PyInstaller bundle
                        if getattr(sys, 'frozen', False):
                            # We're running in a PyInstaller bundle
                            bundle_dir = sys._MEIPASS
                            service_account_path = os.path.join(bundle_dir, service_account_path)
                        else:
                            # We're running in a normal Python environment
                            service_account_path = os.path.join(
                                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                service_account_path
                            )
                    
                    # Initialize Firebase with service account credentials
                    cred = credentials.Certificate(service_account_path)
                    self.firebase_app = firebase_admin.initialize_app(
                        cred,
                        {
                            'databaseURL': firebase_config["databaseURL"]
                        },
                        name='waldorf_db'
                    )
                    self.firebase_initialized = True
                    print("Firebase initialized successfully with service account")
                except Exception as auth_error:
                    print(f"Firebase authentication failed: {str(auth_error)}")
                    print(f"Service account path: {service_account_path}")
                    self.firebase_initialized = False
        except Exception as e:
            print(f"Error initializing Firebase: {str(e)}")
            self.firebase_initialized = False
    
    def load_database(self):
        """Load database from either local file or Firebase"""
        if config.db_config.is_using_local():
            return self._load_from_local()
        elif config.db_config.is_using_firebase():
            return self._load_from_firebase()
        else:
            raise ValueError("No database configuration is enabled")
    
    def _load_from_local(self):
        """Load database from local JSON file"""
        try:
            db_path = config.db_config.get_local_db_path()
            # If path is relative, make it relative to project root
            if not os.path.isabs(db_path):
                # Check if we're running in a PyInstaller bundle
                if getattr(sys, 'frozen', False):
                    # We're running in a PyInstaller bundle, use the current working directory
                    db_path = os.path.join(os.getcwd(), db_path)
                else:
                    # We're running in a normal Python environment
                    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), db_path)
            
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading local database: {str(e)}")
            return {"departments": [], "system_categories": [], "access_permissions": {}}
    
    def _load_from_firebase(self):
        """Load database from Firebase Realtime Database"""
        try:
            if not self.firebase_initialized:
                self._initialize_firebase()
            
            if self.firebase_initialized:
                ref = db.reference('/', app=self.firebase_app)
                data = ref.get()
                if data:
                    return data
                else:
                    print("No data found in Firebase, returning empty structure")
                    return {"departments": [], "system_categories": [], "access_permissions": {}}
            else:
                print("Firebase not initialized, falling back to local database")
                return self._load_from_local()
        except Exception as e:
            print(f"Error loading from Firebase: {str(e)}")
            print("Falling back to local database")
            return self._load_from_local()
    
    def save_database(self, data):
        """Save database to either local file or Firebase"""
        if config.db_config.is_using_local():
            return self._save_to_local(data)
        elif config.db_config.is_using_firebase():
            return self._save_to_firebase(data)
        else:
            raise ValueError("No database configuration is enabled")
    
    def _save_to_local(self, data):
        """Save database to local JSON file"""
        try:
            db_path = config.db_config.get_local_db_path()
            # If path is relative, make it relative to project root
            if not os.path.isabs(db_path):
                # Check if we're running in a PyInstaller bundle
                if getattr(sys, 'frozen', False):
                    # We're running in a PyInstaller bundle, use the current working directory
                    db_path = os.path.join(os.getcwd(), db_path)
                else:
                    # We're running in a normal Python environment
                    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), db_path)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving local database: {str(e)}")
            return False
    
    def _save_to_firebase(self, data):
        """Save database to Firebase Realtime Database"""
        try:
            if not self.firebase_initialized:
                self._initialize_firebase()
            
            if self.firebase_initialized:
                ref = db.reference('/', app=self.firebase_app)
                ref.set(data)
                return True
            else:
                print("Firebase not initialized, cannot save")
                return False
        except Exception as e:
            print(f"Error saving to Firebase: {str(e)}")
            return False
    
    def sync_to_firebase(self):
        """Sync local database to Firebase"""
        if config.db_config.is_using_firebase():
            local_data = self._load_from_local()
            return self._save_to_firebase(local_data)
        else:
            print("Firebase is not enabled in configuration")
            return False
    
    def sync_from_firebase(self):
        """Sync Firebase database to local"""
        if config.db_config.is_using_firebase():
            firebase_data = self._load_from_firebase()
            return self._save_to_local(firebase_data)
        else:
            print("Firebase is not enabled in configuration")
            return False
    
    def switch_database(self, db_type: str):
        """Switch between database types at runtime"""
        try:
            if db_type.lower() == "local":
                config.db_config.switch_to_local()
                # Reinitialize if needed
                if self.firebase_initialized:
                    print("Note: Firebase connection remains active but local database will be used")
            elif db_type.lower() == "firebase":
                config.db_config.switch_to_firebase()
                if not self.firebase_initialized:
                    self._initialize_firebase()
            else:
                print(f"Unknown database type: {db_type}")
                return False
            return True
        except Exception as e:
            print(f"Error switching database: {str(e)}")
            return False
    
    def get_current_database_type(self) -> str:
        """Get the current database type"""
        return config.db_config.database_type.value

# Create a singleton instance
db_manager = DatabaseManager()