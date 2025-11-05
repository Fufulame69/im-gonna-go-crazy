import sys
import os
import json
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QMessageBox, QLineEdit, QComboBox,
                            QRadioButton, QButtonGroup, QDateEdit, QFrame, QGroupBox,
                            QScrollArea, QCheckBox)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# Add the parent directory to the path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Templates.access_template_generator import PDF, create_custom_pdf

class FormScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waldorf Access Form Generator - Sign In and Departure Form")
        self.setGeometry(100, 100, 800, 700)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "waldorf_ico.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Center the window on screen
        self.center_window()
        
        # Load data from database
        self.load_database()
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create UI elements
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the screen"""
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
    def load_database(self):
        """Load data from the database.json file"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "database.json")
            with open(db_path, 'r', encoding='utf-8') as f:
                self.db_data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load database: {str(e)}")
            self.db_data = {"departments": [], "system_categories": []}
    
    def create_widgets(self):
        """Create all UI elements for the form screen"""
        # 1-Main title label: Sign in and departure form
        title_label = QLabel("Sign in and departure form")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Create a scroll area for the form content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)
        
        # 2-Textboxes in order: Name, OnQ user, email, department combobox, position combobox
        self.create_form_fields(form_layout)
        
        # 3- 3 radio buttons: date or arrival, modification date, departure date
        # 4- below the radio buttons, a date picker
        self.create_date_selection(form_layout)
        
        # 5- then two buttons: generate sign in form and next to it the generate departure form
        self.create_action_buttons(form_layout)
        
        scroll_area.setWidget(form_widget)
        self.main_layout.addWidget(scroll_area)
        
        # Navigation bar
        self.create_navigation_bar()
    
    def create_form_fields(self, layout):
        """Create the form input fields"""
        # Group box for personal information
        personal_group = QGroupBox("Personal Information")
        personal_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        personal_layout = QVBoxLayout(personal_group)
        personal_layout.setSpacing(10)
        
        # Name field
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setFixedWidth(100)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        personal_layout.addLayout(name_layout)
        
        # OnQ User field
        onq_layout = QHBoxLayout()
        onq_label = QLabel("OnQ User:")
        onq_label.setFixedWidth(100)
        self.onq_input = QLineEdit()
        self.onq_input.setPlaceholderText("Enter OnQ username")
        onq_layout.addWidget(onq_label)
        onq_layout.addWidget(self.onq_input)
        personal_layout.addLayout(onq_layout)
        
        # Email field
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        email_label.setFixedWidth(100)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        personal_layout.addLayout(email_layout)
        
        # Department combobox
        dept_layout = QHBoxLayout()
        dept_label = QLabel("Department:")
        dept_label.setFixedWidth(100)
        self.department_combo = QComboBox()
        self.department_combo.addItem("Select Department", None)
        for dept in self.db_data.get("departments", []):
            self.department_combo.addItem(dept["name"], dept)
        self.department_combo.currentIndexChanged.connect(self.on_department_changed)
        dept_layout.addWidget(dept_label)
        dept_layout.addWidget(self.department_combo)
        personal_layout.addLayout(dept_layout)
        
        # Position combobox
        pos_layout = QHBoxLayout()
        pos_label = QLabel("Position:")
        pos_label.setFixedWidth(100)
        self.position_combo = QComboBox()
        self.position_combo.addItem("Select Position", None)
        self.position_combo.setEnabled(False)
        pos_layout.addWidget(pos_label)
        pos_layout.addWidget(self.position_combo)
        personal_layout.addLayout(pos_layout)
        
        layout.addWidget(personal_group)
    
    def create_date_selection(self, layout):
        """Create date selection radio buttons and date picker"""
        # Group box for date selection
        date_group = QGroupBox("Date Selection")
        date_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        date_layout = QVBoxLayout(date_group)
        date_layout.setSpacing(10)
        
        # Radio buttons
        radio_layout = QHBoxLayout()
        self.date_radio_group = QButtonGroup()
        
        self.arrival_radio = QRadioButton("Date of Arrival")
        self.arrival_radio.setChecked(True)
        self.date_radio_group.addButton(self.arrival_radio, 0)
        
        self.modification_radio = QRadioButton("Modification Date")
        self.date_radio_group.addButton(self.modification_radio, 1)
        
        self.departure_radio = QRadioButton("Departure Date")
        self.date_radio_group.addButton(self.departure_radio, 2)
        
        radio_layout.addWidget(self.arrival_radio)
        radio_layout.addWidget(self.modification_radio)
        radio_layout.addWidget(self.departure_radio)
        radio_layout.addStretch()
        
        date_layout.addLayout(radio_layout)
        
        # Date picker
        date_picker_layout = QHBoxLayout()
        date_picker_label = QLabel("Select Date:")
        date_picker_label.setFixedWidth(100)
        self.date_picker = QDateEdit()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)
        date_picker_layout.addWidget(date_picker_label)
        date_picker_layout.addWidget(self.date_picker)
        date_picker_layout.addStretch()
        
        date_layout.addLayout(date_picker_layout)
        layout.addWidget(date_group)
    
    def create_action_buttons(self, layout):
        """Create the generate form buttons"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Generate Sign In Form button
        self.signin_button = QPushButton("Generate Sign In Form")
        self.signin_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.signin_button.clicked.connect(self.generate_signin_form)
        button_layout.addWidget(self.signin_button)
        
        # Generate Departure Form button
        self.departure_button = QPushButton("Generate Departure Form")
        self.departure_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.departure_button.clicked.connect(self.generate_departure_form)
        button_layout.addWidget(self.departure_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def create_navigation_bar(self):
        """Create the navigation bar at the bottom of the screen"""
        # Create a frame for the navigation bar with fixed height
        nav_frame = QFrame()
        nav_frame.setFrameStyle(QFrame.Box)
        nav_frame.setFixedHeight(60)  # Fixed height for consistency
        nav_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                border-radius: 5px;
                margin: 2px;
            }
        """)
        
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(15, 8, 15, 8)
        nav_layout.setSpacing(10)
        
        # Access Matrix button
        access_matrix_btn = QPushButton("Access Matrix")
        access_matrix_btn.setFixedHeight(40)  # Fixed height for buttons
        access_matrix_btn.setMinimumWidth(120)  # Minimum width
        access_matrix_btn.setStyleSheet("""
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
        """)
        access_matrix_btn.clicked.connect(self.go_back_to_main)
        nav_layout.addWidget(access_matrix_btn)
        
        # Departments and Positions button
        departments_btn = QPushButton("Departments and Positions")
        departments_btn.setFixedHeight(40)  # Fixed height for buttons
        departments_btn.setMinimumWidth(180)  # Minimum width
        departments_btn.setStyleSheet("""
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
        """)
        departments_btn.clicked.connect(self.go_to_departments)
        nav_layout.addWidget(departments_btn)
        
        # Hotel Systems button
        hotel_systems_btn = QPushButton("Hotel Systems")
        hotel_systems_btn.setFixedHeight(40)  # Fixed height for buttons
        hotel_systems_btn.setMinimumWidth(120)  # Minimum width
        hotel_systems_btn.setStyleSheet("""
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
        """)
        hotel_systems_btn.clicked.connect(self.go_to_hotel_systems)
        nav_layout.addWidget(hotel_systems_btn)
        
        # Form button (current screen)
        form_btn = QPushButton("Form")
        form_btn.setFixedHeight(40)  # Fixed height for buttons
        form_btn.setMinimumWidth(80)  # Minimum width
        form_btn.setStyleSheet("""
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
        """)
        form_btn.setEnabled(False)  # Disable since we're already on this screen
        nav_layout.addWidget(form_btn)
        
        # Add stretch to push exit button to the right
        nav_layout.addStretch()
        
        # Exit button
        exit_button = QPushButton("Exit")
        exit_button.setFixedHeight(40)  # Fixed height for buttons
        exit_button.setMinimumWidth(80)  # Minimum width
        exit_button.setStyleSheet("""
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
        """)
        exit_button.clicked.connect(self.close)
        nav_layout.addWidget(exit_button)
        
        self.main_layout.addWidget(nav_frame)
    
    def on_department_changed(self, index):
        """Handle department selection change"""
        self.position_combo.clear()
        self.position_combo.addItem("Select Position", None)
        
        if index > 0:
            dept_data = self.department_combo.itemData(index)
            if dept_data:
                for position in dept_data.get("positions", []):
                    self.position_combo.addItem(position["name"], position)
                self.position_combo.setEnabled(True)
        else:
            self.position_combo.setEnabled(False)
    
    def get_position_access(self, dept_id, pos_id):
        """Get the access permissions for a specific position"""
        access_permissions = self.db_data.get("access_permissions", {})
        dept_access = access_permissions.get(dept_id, {})
        return dept_access.get(pos_id, {})
    
    def generate_signin_form(self):
        """Generate the sign in form PDF"""
        # Validate form inputs
        name = self.name_input.text().strip()
        onq_user = self.onq_input.text().strip()
        email = self.email_input.text().strip()
        
        if not name or not onq_user or not email:
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields (Name, OnQ User, Email)")
            return
        
        dept_index = self.department_combo.currentIndex()
        pos_index = self.position_combo.currentIndex()
        
        if dept_index <= 0 or pos_index <= 0:
            QMessageBox.warning(self, "Validation Error", "Please select both Department and Position")
            return
        
        dept_data = self.department_combo.itemData(dept_index)
        pos_data = self.position_combo.itemData(pos_index)
        
        if not dept_data or not pos_data:
            QMessageBox.warning(self, "Validation Error", "Invalid department or position selection")
            return
        
        # Get selected date
        selected_date = self.date_picker.date().toString("dd-MMM-yy")
        
        # Get position access permissions
        access_permissions = self.get_position_access(dept_data["id"], pos_data["id"])
        
        # Generate the PDF
        try:
            self.create_signin_pdf(name, onq_user, email, dept_data["name"], pos_data["name"], 
                                selected_date, access_permissions)
            QMessageBox.information(self, "Success", f"Sign in form generated successfully for {name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate sign in form: {str(e)}")
    
    def generate_departure_form(self):
        """Generate the departure form PDF (placeholder for now)"""
        QMessageBox.information(self, "Info", "Departure form generation is not implemented yet")
    
    def create_signin_pdf(self, name, onq_user, email, department, position, date, access_permissions):
        """Create the sign in form PDF using the template"""
        # Get system categories from database
        system_categories = self.db_data.get("system_categories", [])
        
        # Create the custom PDF
        pdf = create_custom_pdf(name, onq_user, email, department, position, date,
                             access_permissions, system_categories)
        
        if pdf:
            # Save the PDF
            output_filename = f"sign_in_form_{name.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(output_filename)
            return output_filename
        return None
    
    
    def go_back_to_main(self):
        """Go back to the main screen"""
        # Import here to avoid circular import
        try:
            from GUI.main_screen import MainScreen
            self.main_screen = MainScreen()
            self.main_screen.show()
            self.close()  # Close the current screen
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to import main screen: {str(e)}")
    
    def go_to_departments(self):
        """Go to the departments and positions screen"""
        # Import here to avoid circular import
        try:
            from GUI.departments_and_positions import DepartmentsAndPositionsScreen
            self.departments_screen = DepartmentsAndPositionsScreen()
            self.departments_screen.show()
            self.close()  # Close the current screen
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to import departments screen: {str(e)}")
    
    def go_to_hotel_systems(self):
        """Go to the hotel systems screen"""
        # Import here to avoid circular import
        try:
            from GUI.hotel_systems import HotelSystemsScreen
            self.hotel_systems_screen = HotelSystemsScreen()
            self.hotel_systems_screen.show()
            self.close()  # Close the current screen
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to import hotel systems screen: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    screen = FormScreen()
    screen.show()
    sys.exit(app.exec_())