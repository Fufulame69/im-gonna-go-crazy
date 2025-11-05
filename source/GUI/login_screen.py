import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon

# Add the parent directory to the path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waldorf Access Form Generator")
        self.setFixedSize(500, 420)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "waldorf_ico.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Center the window on screen
        self.center_window()
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #2c3e50;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 12pt;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create UI elements
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the screen"""
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
    def create_widgets(self):
        """Create all UI elements for the login screen"""
        # Title
        title_label = QLabel("Waldorf Access Form Generator")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin: 10px 0;")
        self.main_layout.addWidget(title_label)
        
        # Logo
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignCenter)
        
        try:
            # Try to load the logo if it exists
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "waldorf_logo.png")
            if os.path.exists(logo_path):
                logo_pixmap = QPixmap(logo_path)
                logo_pixmap = logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label = QLabel()
                logo_label.setPixmap(logo_pixmap)
                logo_label.setAlignment(Qt.AlignCenter)
                logo_layout.addWidget(logo_label)
            else:
                # If logo doesn't exist, show a placeholder
                logo_placeholder = QLabel("[LOGO]")
                logo_placeholder.setAlignment(Qt.AlignCenter)
                logo_placeholder.setFont(QFont("Arial", 24))
                logo_placeholder.setStyleSheet("color: #7f8c8d; border: 2px dashed #bdc3c7; padding: 20px;")
                logo_placeholder.setFixedSize(150, 150)
                logo_layout.addWidget(logo_placeholder)
        except Exception as e:
            # If there's an error loading the logo, show a placeholder
            logo_placeholder = QLabel("[LOGO]")
            logo_placeholder.setAlignment(Qt.AlignCenter)
            logo_placeholder.setFont(QFont("Arial", 24))
            logo_placeholder.setStyleSheet("color: #7f8c8d; border: 2px dashed #bdc3c7; padding: 20px;")
            logo_placeholder.setFixedSize(150, 150)
            logo_layout.addWidget(logo_placeholder)
            
        self.main_layout.addWidget(logo_container)
        
        # Username label and entry
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 12))
        self.main_layout.addWidget(username_label)
        
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Enter username")
        self.main_layout.addWidget(self.username_entry)
        
        # Password label and entry
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 12))
        self.main_layout.addWidget(password_label)
        
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Enter password")
        self.main_layout.addWidget(self.password_entry)
        
        # Login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        self.main_layout.addWidget(login_button)
        
        # Set focus to username field
        self.username_entry.setFocus()
        
        # Enable Enter key for login
        self.password_entry.returnPressed.connect(self.login)
        
    def login(self):
        """Validate login credentials"""
        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()
        
        # For now, use hardcoded admin credentials
        if username == "admin" and password == "admin":
            QMessageBox.information(self, "Login Successful", "Welcome to Waldorf Access Form Generator!")
            self.open_main_screen()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")
            self.password_entry.clear()
            self.password_entry.setFocus()
            
    def open_main_screen(self):
        """Open the main application screen"""
        try:
            from GUI import main_screen
            self.hide()  # Hide instead of close
            self.main_window = main_screen.MainScreen()
            self.main_window.show()
        except ImportError as e:
            # If main_screen is not implemented yet, just show a message
            QMessageBox.warning(self, "Import Error", f"Failed to import main screen: {str(e)}")
            self.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error opening main screen: {str(e)}")
            self.show()  # Show login screen again if there's an error
            
    def run(self):
        """Start the login screen"""
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    login = LoginScreen()
    login.run()
    sys.exit(app.exec_())