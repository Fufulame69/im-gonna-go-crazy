import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

# Add the source directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "source"))

def main():
    """Main entry point for the Waldorf Access Form Generator application"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set the application icon
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "waldorf_ico.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Import and run the login screen
    from GUI import login_screen
    login = login_screen.LoginScreen()
    login.run()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()