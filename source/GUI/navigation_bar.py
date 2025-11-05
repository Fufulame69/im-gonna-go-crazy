import sys
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class NavigationBar(QFrame):
    """Shared navigation bar component for all screens"""
    
    def __init__(self, parent=None, current_screen="main"):
        super().__init__(parent)
        self.current_screen = current_screen
        self.parent_window = parent
        self.setFrameStyle(QFrame.Box)
        self.setFixedHeight(60)  # Fixed height for consistency
        self.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                border-radius: 5px;
                margin: 2px;
            }
        """)
        
        self.create_layout()
        self.create_buttons()
    
    def create_layout(self):
        """Create the navigation bar layout"""
        self.nav_layout = QHBoxLayout(self)
        self.nav_layout.setContentsMargins(15, 8, 15, 8)
        self.nav_layout.setSpacing(10)
    
    def create_buttons(self):
        """Create navigation buttons"""
        # Access Matrix button
        self.access_matrix_btn = QPushButton("Access Matrix")
        self.access_matrix_btn.setFixedHeight(40)  # Fixed height for buttons
        self.access_matrix_btn.setMinimumWidth(120)  # Minimum width
        self.access_matrix_btn.clicked.connect(self.go_to_main)
        
        # Departments and Positions button
        self.departments_btn = QPushButton("Departments and Positions")
        self.departments_btn.setFixedHeight(40)  # Fixed height for buttons
        self.departments_btn.setMinimumWidth(180)  # Minimum width
        self.departments_btn.clicked.connect(self.go_to_departments)
        
        # Hotel Systems button
        self.hotel_systems_btn = QPushButton("Hotel Systems")
        self.hotel_systems_btn.setFixedHeight(40)  # Fixed height for buttons
        self.hotel_systems_btn.setMinimumWidth(120)  # Minimum width
        self.hotel_systems_btn.clicked.connect(self.go_to_hotel_systems)
        
        # Form button
        self.form_btn = QPushButton("Form")
        self.form_btn.setFixedHeight(40)  # Fixed height for buttons
        self.form_btn.setMinimumWidth(80)  # Minimum width
        self.form_btn.clicked.connect(self.go_to_form)
        
        # Exit button
        self.exit_button = QPushButton("Exit")
        self.exit_button.setFixedHeight(40)  # Fixed height for buttons
        self.exit_button.setMinimumWidth(80)  # Minimum width
        self.exit_button.clicked.connect(self.exit_application)
        
        # Add buttons to layout
        self.nav_layout.addWidget(self.access_matrix_btn)
        self.nav_layout.addWidget(self.departments_btn)
        self.nav_layout.addWidget(self.hotel_systems_btn)
        self.nav_layout.addWidget(self.form_btn)
        
        # Add stretch to push exit button to the right
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.exit_button)
        
        # Set button styles based on current screen
        self.update_button_styles()
    
    def update_button_styles(self):
        """Update button styles based on the current screen"""
        # Common button style for inactive buttons
        inactive_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        
        # Style for the active/current screen button
        active_style = """
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #1a252f;
            }
        """
        
        # Style for exit button
        exit_style = """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        
        # Apply styles based on current screen
        if self.current_screen == "main":
            self.access_matrix_btn.setStyleSheet(active_style)
            self.access_matrix_btn.setEnabled(False)
        else:
            self.access_matrix_btn.setStyleSheet(inactive_style)
            self.access_matrix_btn.setEnabled(True)
        
        if self.current_screen == "departments":
            self.departments_btn.setStyleSheet(active_style)
            self.departments_btn.setEnabled(False)
        else:
            self.departments_btn.setStyleSheet(inactive_style)
            self.departments_btn.setEnabled(True)
        
        if self.current_screen == "hotel_systems":
            self.hotel_systems_btn.setStyleSheet(active_style)
            self.hotel_systems_btn.setEnabled(False)
        else:
            self.hotel_systems_btn.setStyleSheet(inactive_style)
            self.hotel_systems_btn.setEnabled(True)
        
        if self.current_screen == "form":
            self.form_btn.setStyleSheet(active_style)
            self.form_btn.setEnabled(False)
        else:
            self.form_btn.setStyleSheet(inactive_style)
            self.form_btn.setEnabled(True)
        
        # Exit button always has the same style
        self.exit_button.setStyleSheet(exit_style)
    
    def go_to_main(self):
        """Navigate to main screen"""
        if self.current_screen != "main":
            try:
                from GUI.main_screen import MainScreen
                main_screen = MainScreen()
                main_screen.show()
                if self.parent_window:
                    self.parent_window.close()
            except ImportError as e:
                print(f"Failed to import main screen: {str(e)}")
    
    def go_to_departments(self):
        """Navigate to departments and positions screen"""
        if self.current_screen != "departments":
            try:
                from GUI.departments_and_positions import DepartmentsAndPositionsScreen
                departments_screen = DepartmentsAndPositionsScreen()
                departments_screen.show()
                if self.parent_window:
                    self.parent_window.close()
            except ImportError as e:
                print(f"Failed to import departments screen: {str(e)}")
    
    def go_to_hotel_systems(self):
        """Navigate to hotel systems screen"""
        if self.current_screen != "hotel_systems":
            try:
                from GUI.hotel_systems import HotelSystemsScreen
                hotel_systems_screen = HotelSystemsScreen()
                hotel_systems_screen.show()
                if self.parent_window:
                    self.parent_window.close()
            except ImportError as e:
                print(f"Failed to import hotel systems screen: {str(e)}")
    
    def go_to_form(self):
        """Navigate to form screen"""
        if self.current_screen != "form":
            try:
                from GUI.Form import FormScreen
                form_screen = FormScreen()
                form_screen.show()
                if self.parent_window:
                    self.parent_window.close()
            except ImportError as e:
                print(f"Failed to import form screen: {str(e)}")
    
    def exit_application(self):
        """Exit the application"""
        if self.parent_window:
            self.parent_window.close()