#!/usr/bin/env python3
"""
Test script to verify database manager works with both local and Firebase configurations
"""

import sys
import os

# Add the source directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "source"))

# Import the database manager and config
from database.db_manager import db_manager
import config

def test_local_database():
    """Test local database operations"""
    print("Testing LOCAL database operations...")
    
    # Load data
    print("Loading data from local database...")
    data = db_manager.load_database()
    print(f"Loaded {len(data.get('departments', []))} departments")
    print(f"Loaded {len(data.get('system_categories', []))} system categories")
    
    # Test saving
    print("Saving test data to local database...")
    success = db_manager.save_database(data)
    print(f"Save operation {'succeeded' if success else 'failed'}")
    
    return success

def test_firebase_database():
    """Test Firebase database operations"""
    print("\nTesting FIREBASE database operations...")
    
    # Temporarily enable Firebase
    original_local = config.USING_LOCAL_DB
    original_firebase = config.USING_FIREBASE_REALTIME_DB
    
    config.USING_LOCAL_DB = False
    config.USING_FIREBASE_REALTIME_DB = True
    
    try:
        # Load data
        print("Loading data from Firebase...")
        data = db_manager.load_database()
        print(f"Loaded {len(data.get('departments', []))} departments")
        print(f"Loaded {len(data.get('system_categories', []))} system categories")
        
        # Test saving
        print("Saving test data to Firebase...")
        success = db_manager.save_database(data)
        print(f"Save operation {'succeeded' if success else 'failed'}")
        
        return success
    except Exception as e:
        print(f"Firebase test failed with error: {str(e)}")
        return False
    finally:
        # Restore original configuration
        config.USING_LOCAL_DB = original_local
        config.USING_FIREBASE_REALTIME_DB = original_firebase

def main():
    """Main test function"""
    print("=" * 50)
    print("DATABASE MANAGER TEST SCRIPT")
    print("=" * 50)
    
    # Test local database
    local_success = test_local_database()
    
    # Test Firebase database
    firebase_success = test_firebase_database()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Local database test: {'PASSED' if local_success else 'FAILED'}")
    print(f"Firebase database test: {'PASSED' if firebase_success else 'FAILED'}")
    
    if local_success:
        print("\n[SUCCESS] Local database operations are working correctly")
    else:
        print("\n[FAILED] Local database operations have issues")
    
    if firebase_success:
        print("[SUCCESS] Firebase database operations are working correctly")
    else:
        print("[FAILED] Firebase database operations have issues")
    
    print("\nTo use Firebase in the main application:")
    print("1. Set USING_LOCAL_DB = False in config.py")
    print("2. Set USING_FIREBASE_REALTIME_DB = True in config.py")
    print("3. Ensure you have internet connectivity")
    print("4. Run the application normally")

if __name__ == "__main__":
    main()