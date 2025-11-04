import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QMessageBox, 
                            QTreeWidget, QTreeWidgetItem, QScrollArea, QGroupBox,
                            QCheckBox, QSplitter, QFrame, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

# Add the parent directory to the path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DepartmentsAndPositionsScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waldorf Access Form Generator - Departments and Positions")
        self.setGeometry(100, 100, 1200, 800)
        
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
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                font-size: 10pt;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
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
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        
        # Load data from database
        self.load_database()
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
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
        """Create all UI elements for the departments and positions screen"""
        # Title
        title_label = QLabel("Departments and Positions Management")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Create a test table to display departments and positions
        self.create_test_table()
        
        # Navigation bar
        self.create_navigation_bar()
    
    def create_test_table(self):
        """Create a test table to display departments and positions"""
        # Create a group box for the table
        table_group = QGroupBox("Departments and Positions")
        table_layout = QVBoxLayout(table_group)
        
        # Create table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Department", "Position", "Actions"])
        
        # Populate table with data
        row_count = 0
        for dept in self.db_data.get("departments", []):
            for position in dept.get("positions", []):
                self.table_widget.insertRow(row_count)
                
                # Department name
                dept_item = QTableWidgetItem(dept["name"])
                self.table_widget.setItem(row_count, 0, dept_item)
                
                # Position name
                pos_item = QTableWidgetItem(position["name"])
                self.table_widget.setItem(row_count, 1, pos_item)
                
                # Actions button
                actions_btn = QPushButton("Edit")
                actions_btn.clicked.connect(lambda checked, r=row_count: self.edit_position(r))
                self.table_widget.setCellWidget(row_count, 2, actions_btn)
                
                row_count += 1
        
        # Adjust column widths
        self.table_widget.setColumnWidth(0, 300)
        self.table_widget.setColumnWidth(1, 300)
        self.table_widget.setColumnWidth(2, 100)
        
        # Add table to layout
        table_layout.addWidget(self.table_widget)
        
        # Add some test buttons
        button_layout = QHBoxLayout()
        
        add_dept_btn = QPushButton("Add Department")
        add_dept_btn.clicked.connect(self.add_department)
        button_layout.addWidget(add_dept_btn)
        
        add_pos_btn = QPushButton("Add Position")
        add_pos_btn.clicked.connect(self.add_position)
        button_layout.addWidget(add_pos_btn)
        
        button_layout.addStretch()
        
        table_layout.addLayout(button_layout)
        self.main_layout.addWidget(table_group)
    
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
        
        # Departments and Positions button (current screen)
        departments_btn = QPushButton("Departments and Positions")
        departments_btn.setFixedHeight(40)  # Fixed height for buttons
        departments_btn.setMinimumWidth(180)  # Minimum width
        departments_btn.setStyleSheet("""
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
        departments_btn.setEnabled(False)  # Disable since we're already on this screen
        nav_layout.addWidget(departments_btn)
        
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
    
    def go_back_to_main(self):
        """Go back to the main screen"""
        # Import here to avoid circular import
        try:
            from main_screen import MainScreen
            self.main_screen = MainScreen()
            self.main_screen.show()
            self.close()  # Close the current screen
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to import main screen: {str(e)}")
    
    def edit_position(self, row):
        """Edit a position (test function)"""
        dept_name = self.table_widget.item(row, 0).text()
        pos_name = self.table_widget.item(row, 1).text()
        QMessageBox.information(self, "Edit Position", f"Editing position: {pos_name} in {dept_name}")
    
    def add_department(self):
        """Add a new department (test function)"""
        QMessageBox.information(self, "Add Department", "This is a test function for adding a department")
    
    def add_position(self):
        """Add a new position (test function)"""
        QMessageBox.information(self, "Add Position", "This is a test function for adding a position")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    screen = DepartmentsAndPositionsScreen()
    screen.show()
    sys.exit(app.exec_())