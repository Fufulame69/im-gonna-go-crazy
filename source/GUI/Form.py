import sys
import os
import json
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QMessageBox, QLineEdit, QComboBox,
                            QRadioButton, QButtonGroup, QDateEdit, QFrame, QGroupBox,
                            QScrollArea, QCheckBox, QFileDialog)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# Add the parent directory to the path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Templates.access_template_generator import PDF, create_custom_pdf
from Templates.departure_template import SeparationChecklistPDF

# Import navigation bar
from GUI.navigation_bar import NavigationBar

class FormScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waldorf Access Form Generator - Sign In and Departure Form")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "waldorf_ico.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Center the window on screen
        self.center_window()
        
        # Initialize configuration and paths
        self.config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
        self.generated_forms_dir = None
        self.persons_data = {}
        
        # Load configuration
        self.load_config()
        
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
        
    def load_config(self):
        """Load configuration from config.json file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.generated_forms_dir = config.get("generated_forms_dir", None)
        except Exception as e:
            QMessageBox.warning(self, "Config Warning", f"Failed to load config: {str(e)}")
    
    def save_config(self):
        """Save configuration to config.json file"""
        try:
            config = {
                "generated_forms_dir": self.generated_forms_dir
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "Config Warning", f"Failed to save config: {str(e)}")
    
    def load_database(self):
        """Load data from the database.json file"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "database.json")
            with open(db_path, 'r', encoding='utf-8') as f:
                self.db_data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load database: {str(e)}")
            self.db_data = {"departments": [], "system_categories": []}
        
        # Load persons data if generated_forms_dir exists
        if self.generated_forms_dir:
            self.load_persons_data()
    
    def load_persons_data(self):
        """Load persons data from the JSON tracking file"""
        try:
            persons_file = os.path.join(self.generated_forms_dir, "persons.json")
            if os.path.exists(persons_file):
                with open(persons_file, 'r', encoding='utf-8') as f:
                    self.persons_data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Data Warning", f"Failed to load persons data: {str(e)}")
            self.persons_data = {}
    
    def create_widgets(self):
        """Create all UI elements for the form screen"""
        # 1-Main title label: Sign in and departure form
        title_label = QLabel("Sign in and departure form")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Directory selection section
        self.create_directory_selection(self.main_layout)
        
        # Create a scroll area for the form content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)
        
        # Person selection section
        self.create_person_selection(form_layout)
        
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
    
    def create_directory_selection(self, layout):
        """Create directory selection UI components"""
        # Group box for directory selection
        dir_group = QGroupBox("Generated Forms Directory")
        dir_group.setStyleSheet("""
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
        dir_layout = QHBoxLayout(dir_group)
        dir_layout.setSpacing(10)
        
        # Directory label
        dir_label = QLabel("Please pick a directory where you would like the generations to be:")
        dir_layout.addWidget(dir_label)
        
        # Directory path display
        self.dir_path_label = QLabel("No directory selected")
        self.dir_path_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        if self.generated_forms_dir:
            self.dir_path_label.setText(self.generated_forms_dir)
            self.dir_path_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        dir_layout.addWidget(self.dir_path_label)
        
        # Browse button
        self.browse_button = QPushButton("Browse")
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.browse_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.browse_button)
        
        layout.addWidget(dir_group)
    
    def create_person_selection(self, layout):
        """Create person selection UI components"""
        # Group box for person selection
        person_group = QGroupBox("Person Selection")
        person_group.setStyleSheet("""
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
        person_layout = QHBoxLayout(person_group)
        person_layout.setSpacing(10)
        
        # Person selection label
        person_label = QLabel("Select Person:")
        person_label.setFixedWidth(100)
        person_layout.addWidget(person_label)
        
        # Person combobox (editable for searching)
        self.person_combo = QComboBox()
        self.person_combo.setEditable(True)
        self.person_combo.setInsertPolicy(QComboBox.NoInsert)  # Don't insert typed text as new item
        # Start with empty combobox
        self.person_combo.setPlaceholderText("Type to search or enter new person name...")
        # Load existing persons if directory is selected
        if self.generated_forms_dir and self.persons_data:
            for person_id, person_info in self.persons_data.items():
                display_text = f"{person_info['name']} ({person_info['email']})"
                self.person_combo.addItem(display_text, person_id)
        
        self.person_combo.currentIndexChanged.connect(self.on_person_changed)
        self.person_combo.editTextChanged.connect(self.on_person_text_changed)
        # Install event filter for key press events
        self.person_combo.installEventFilter(self)
        person_layout.addWidget(self.person_combo)
        
        layout.addWidget(person_group)
    
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
        onq_label = QLabel("OnQ User (Optional):")
        onq_label.setFixedWidth(100)
        self.onq_input = QLineEdit()
        self.onq_input.setPlaceholderText("Enter OnQ username (optional)")
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
        nav_bar = NavigationBar(self, "form")
        self.main_layout.addWidget(nav_bar)
    
    def browse_directory(self):
        """Open directory browser to select generated forms directory"""
        selected_dir = QFileDialog.getExistingDirectory(self, "Select Generated Forms Directory")
        if selected_dir:
            # Create generated_forms subdirectory
            self.generated_forms_dir = os.path.join(selected_dir, "generated_forms")
            try:
                os.makedirs(self.generated_forms_dir, exist_ok=True)
                self.dir_path_label.setText(self.generated_forms_dir)
                self.dir_path_label.setStyleSheet("color: #27ae60; font-weight: bold;")
                
                # Save configuration
                self.save_config()
                
                # Load persons data
                self.load_persons_data()
                
                # Update person combobox
                self.update_person_combo()
                
                QMessageBox.information(self, "Success", f"Directory set to: {self.generated_forms_dir}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create directory: {str(e)}")
    
    def update_person_combo(self):
        """Update the person combobox with loaded persons data"""
        current_selection = self.person_combo.currentData()
        current_text = self.person_combo.currentText()
        self.person_combo.clear()
        self.person_combo.setEditable(True)
        self.person_combo.setInsertPolicy(QComboBox.NoInsert)
        self.person_combo.setPlaceholderText("Type to search or enter new person name...")
        
        if self.persons_data:
            for person_id, person_info in self.persons_data.items():
                display_text = f"{person_info['name']} ({person_info['email']})"
                self.person_combo.addItem(display_text, person_id)
            
            # Restore previous selection if possible
            for i in range(self.person_combo.count()):
                if self.person_combo.itemData(i) == current_selection:
                    self.person_combo.setCurrentIndex(i)
                    break
            else:
                # If no matching data found, restore the text
                self.person_combo.setEditText(current_text)
    
    def on_person_changed(self, index):
        """Handle person selection change"""
        person_id = self.person_combo.itemData(index)
        if person_id and person_id in self.persons_data:
            person_info = self.persons_data[person_id]
            # Fill form fields with person's data
            self.name_input.setText(person_info['name'])
            self.email_input.setText(person_info['email'])
            # Clear other fields that should be filled fresh
            self.onq_input.clear()
            self.department_combo.setCurrentIndex(0)
            self.position_combo.setCurrentIndex(0)
            # For existing users, default to modification date
            self.modification_radio.setChecked(True)
    
    def on_person_text_changed(self, text):
        """Handle text change in person combobox for searching/filtering"""
        if not text.strip():
            # If text is empty, just return - don't reset anything
            return
        
        # Search for matching person
        text_lower = text.lower()
        for i in range(self.person_combo.count()):
            item_text = self.person_combo.itemText(i)
            if text_lower in item_text.lower():
                # Found a match, but don't automatically select to allow user to continue typing
                return
        
        # If no exact match found, user might be typing a new person name
        # We don't automatically clear the form to allow continuous typing
    
    def eventFilter(self, obj, event):
        """Event filter to handle key press events in the person combobox"""
        if obj == self.person_combo and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # Get current text
                current_text = self.person_combo.currentText().strip()
                
                # Check if the text matches an existing person
                for i in range(self.person_combo.count()):
                    item_text = self.person_combo.itemText(i)
                    if current_text.lower() == item_text.lower():
                        # Exact match found, select this person
                        self.person_combo.blockSignals(True)
                        self.person_combo.setCurrentIndex(i)
                        self.person_combo.blockSignals(False)
                        self.on_person_changed(i)
                        return True
                
                # No exact match, check if it's a partial match
                for i in range(self.person_combo.count()):
                    item_text = self.person_combo.itemText(i)
                    if current_text.lower() in item_text.lower():
                        # Partial match found, select this person
                        self.person_combo.blockSignals(True)
                        self.person_combo.setCurrentIndex(i)
                        self.person_combo.blockSignals(False)
                        self.on_person_changed(i)
                        return True
                
                # No match found, just accept the text as is
                return True
        
        return super().eventFilter(obj, event)
    
    def clear_form_fields(self):
        """Clear all form input fields"""
        self.name_input.clear()
        self.onq_input.clear()
        self.email_input.clear()
        self.department_combo.setCurrentIndex(0)
        self.position_combo.setCurrentIndex(0)
    
    def save_person_data(self, name, email):
        """Save person data to the JSON tracking file"""
        if not self.generated_forms_dir:
            return None
        
        # Generate a unique person ID
        person_id = name.lower().replace(' ', '_') + '_' + str(len(self.persons_data))
        
        # Add to persons data
        self.persons_data[person_id] = {
            'name': name,
            'email': email,
            'created_date': datetime.datetime.now().isoformat()
        }
        
        # Save to file
        try:
            persons_file = os.path.join(self.generated_forms_dir, "persons.json")
            with open(persons_file, 'w', encoding='utf-8') as f:
                json.dump(self.persons_data, f, indent=2)
            return person_id
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to save person data: {str(e)}")
            return None
    
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
        # Check if directory is selected
        if not self.generated_forms_dir:
            QMessageBox.warning(self, "Directory Required", "Please select a directory for generated forms first")
            return
        
        # Validate form inputs
        name = self.name_input.text().strip()
        onq_user = self.onq_input.text().strip()
        email = self.email_input.text().strip()
        
        if not name or not email:
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields (Name, Email)")
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
        
        # Check if this is a new person or existing person
        person_id = self.person_combo.currentData()
        
        if not person_id:
            # Save new person data
            person_id = self.save_person_data(name, email)
            if person_id:
                # Update the person combobox
                self.update_person_combo()
                # Select the newly added person
                for i in range(self.person_combo.count()):
                    if self.person_combo.itemData(i) == person_id:
                        self.person_combo.setCurrentIndex(i)
                        break
        
        # Generate the PDF
        try:
            output_path = self.create_signin_pdf(name, onq_user, email, dept_data["name"], pos_data["name"],
                                               selected_date, access_permissions, person_id)
            if output_path:
                QMessageBox.information(self, "Success", f"Sign in form generated successfully for {name}\nSaved to: {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate sign in form: {str(e)}")
    
    def generate_departure_form(self):
        """Generate the departure form PDF"""
        # Check if directory is selected
        if not self.generated_forms_dir:
            QMessageBox.warning(self, "Directory Required", "Please select a directory for generated forms first")
            return
        
        # Validate form inputs
        name = self.name_input.text().strip()
        onq_user = self.onq_input.text().strip()
        email = self.email_input.text().strip()
        
        if not name or not email:
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields (Name, Email)")
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
        
        # Check if this is a new person or existing person
        person_id = self.person_combo.currentData()
        
        if not person_id:
            # Save new person data
            person_id = self.save_person_data(name, email)
            if person_id:
                # Update the person combobox
                self.update_person_combo()
                # Select the newly added person
                for i in range(self.person_combo.count()):
                    if self.person_combo.itemData(i) == person_id:
                        self.person_combo.setCurrentIndex(i)
                        break
        
        # Get position access permissions
        access_permissions = self.get_position_access(dept_data["id"], pos_data["id"])
        
        # Get system categories from database
        system_categories = self.db_data.get("system_categories", [])
        
        # Generate the PDF
        try:
            output_path = self.create_departure_pdf(name, onq_user, email, dept_data["name"], pos_data["name"],
                                                  selected_date, person_id, access_permissions, system_categories)
            if output_path:
                QMessageBox.information(self, "Success", f"Departure form generated successfully for {name}\nSaved to: {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate departure form: {str(e)}")
    
    def create_signin_pdf(self, name, onq_user, email, department, position, date, access_permissions, person_id):
        """Create the sign in form PDF using the template"""
        # Get system categories from database
        system_categories = self.db_data.get("system_categories", [])
        
        # Create the custom PDF
        pdf = create_custom_pdf(name, onq_user, email, department, position, date,
                             access_permissions, system_categories)
        
        if pdf:
            # Create person folder if it doesn't exist
            person_folder_name = name.replace(' ', '_')
            person_folder_path = os.path.join(self.generated_forms_dir, person_folder_name)
            os.makedirs(person_folder_path, exist_ok=True)
            
            # Generate unique filename with timestamp
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"sign_in_form_{timestamp}.pdf"
            output_path = os.path.join(person_folder_path, output_filename)
            
            # Save the PDF
            pdf.output(output_path)
            return output_path
        return None
    
    def create_departure_pdf(self, name, onq_user, email, department, position, date, person_id, access_permissions, system_categories):
        """Create the departure form PDF using the departure template"""
        # Create the custom departure PDF
        pdf = SeparationChecklistPDF(orientation='P', unit='mm', format='A4')
        
        if pdf:
            # Create person folder if it doesn't exist
            person_folder_name = name.replace(' ', '_')
            person_folder_path = os.path.join(self.generated_forms_dir, person_folder_name)
            os.makedirs(person_folder_path, exist_ok=True)
            
            # Generate unique filename with timestamp
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"departure_form_{timestamp}.pdf"
            output_path = os.path.join(person_folder_path, output_filename)
            
            # Generate the checklist with employee data
            pdf.generate_checklist(name, onq_user, department, position, date, access_permissions, system_categories)
            
            # Save the PDF
            pdf.output(output_path)
            return output_path
        return None
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    screen = FormScreen()
    screen.show()
    sys.exit(app.exec_())