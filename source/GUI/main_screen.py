import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QPushButton, QMessageBox,
                            QTreeWidget, QTreeWidgetItem, QScrollArea, QGroupBox,
                            QCheckBox, QSplitter, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

# Add the parent directory to the path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import departments and positions screen
from departments_and_positions import DepartmentsAndPositionsScreen

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waldorf Access Form Generator - Access Matrix")
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
            QTreeWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                font-size: 10pt;
            }
            QTreeWidget::item {
                padding: 3px;
            }
            QTreeWidget::item:selected {
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
            QCheckBox {
                font-size: 9pt;
                spacing: 5px;
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
        
        # Store access permissions
        self.access_permissions = {}
        
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
    
    def save_permissions_to_database(self, dept_id, position_id, category_id, system_id, is_checked):
        """Save or remove permission in the database"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "database.json")
            
            # Load current database
            with open(db_path, 'r', encoding='utf-8') as f:
                db_data = json.load(f)
            
            # Initialize access_permissions if not exists
            if "access_permissions" not in db_data:
                db_data["access_permissions"] = {}
            
            # Create department key if not exists
            if dept_id not in db_data["access_permissions"]:
                db_data["access_permissions"][dept_id] = {}
            
            # Create position key if not exists
            if position_id not in db_data["access_permissions"][dept_id]:
                db_data["access_permissions"][dept_id][position_id] = {}
            
            # Create category key if not exists
            if category_id not in db_data["access_permissions"][dept_id][position_id]:
                db_data["access_permissions"][dept_id][position_id][category_id] = {}
            
            if is_checked:
                # Add the system permission
                db_data["access_permissions"][dept_id][position_id][category_id][system_id] = True
            else:
                # Remove the system permission if it exists
                if system_id in db_data["access_permissions"][dept_id][position_id][category_id]:
                    del db_data["access_permissions"][dept_id][position_id][category_id][system_id]
                
                # Clean up empty structures
                if not db_data["access_permissions"][dept_id][position_id][category_id]:
                    del db_data["access_permissions"][dept_id][position_id][category_id]
                
                if not db_data["access_permissions"][dept_id][position_id]:
                    del db_data["access_permissions"][dept_id][position_id]
                
                if not db_data["access_permissions"][dept_id]:
                    del db_data["access_permissions"][dept_id]
            
            # Save updated database
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(db_data, f, indent=2, ensure_ascii=False)
            
            # Update in-memory data
            self.db_data = db_data
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save permissions to database: {str(e)}")
    
    def load_permissions_from_database(self, dept_id, position_id):
        """Load permissions for a specific position from the database"""
        try:
            if "access_permissions" not in self.db_data:
                return {}
            
            if dept_id not in self.db_data["access_permissions"]:
                return {}
            
            if position_id not in self.db_data["access_permissions"][dept_id]:
                return {}
            
            return self.db_data["access_permissions"][dept_id][position_id]
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load permissions from database: {str(e)}")
            return {}
            
    def create_widgets(self):
        """Create all UI elements for the main screen"""
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Departments and Positions
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Systems
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (30% left, 70% right)
        splitter.setSizes([360, 840])
        
        self.main_layout.addWidget(splitter)
        
        # Navigation bar
        self.create_navigation_bar()
        
    def create_left_panel(self):
        """Create the left panel with departments and positions tree"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to extend to top
        
        # Title
        left_title = QLabel("Departments and Positions")
        left_title.setFont(QFont("Arial", 12, QFont.Bold))
        left_title.setStyleSheet("color: #2c3e50; padding: 5px;")
        left_layout.addWidget(left_title)
        
        # Tree widget for departments and positions
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Organization Structure")
        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
        
        # Populate tree with departments and positions
        for dept in self.db_data.get("departments", []):
            dept_item = QTreeWidgetItem(self.tree_widget)
            dept_item.setText(0, dept["name"])
            dept_item.setData(0, Qt.UserRole, {"type": "department", "id": dept["id"]})
            
            for position in dept.get("positions", []):
                pos_item = QTreeWidgetItem(dept_item)
                pos_item.setText(0, position["name"])
                pos_item.setData(0, Qt.UserRole, {"type": "position", "id": position["id"], "dept_id": dept["id"]})
        
        self.tree_widget.expandAll()
        left_layout.addWidget(self.tree_widget)
        
        return left_widget
        
    def create_right_panel(self):
        """Create the right panel with system categories and checkboxes"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to extend to top
        
        # Title
        right_title = QLabel("System Access Permissions")
        right_title.setFont(QFont("Arial", 12, QFont.Bold))
        right_title.setStyleSheet("color: #2c3e50; padding: 5px;")
        right_layout.addWidget(right_title)
        
        # Scroll area for system categories
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Container widget for system categories
        self.systems_container = QWidget()
        self.systems_layout = QVBoxLayout(self.systems_container)
        
        # Create system category groups
        self.system_checkboxes = {}
        for category in self.db_data.get("system_categories", []):
            group_box = QGroupBox(category["name"])
            
            # Use a 2-column layout for systems
            group_layout = QVBoxLayout()
            columns_layout = QHBoxLayout()
            
            # Create two columns for checkboxes
            left_column = QVBoxLayout()
            right_column = QVBoxLayout()
            
            # Create checkboxes for systems in this category
            category_checkboxes = {}
            systems = category.get("systems", [])
            
            # Split systems between two columns
            for i, system in enumerate(systems):
                checkbox = QCheckBox(system["name"])
                checkbox.stateChanged.connect(self.on_checkbox_changed)
                # Store data as a property instead of using setData
                checkbox.category_id = category["id"]
                checkbox.system_id = system["id"]
                category_checkboxes[system["id"]] = checkbox
                
                # Add to appropriate column
                if i % 2 == 0:
                    left_column.addWidget(checkbox)
                else:
                    right_column.addWidget(checkbox)
            
            # Add columns to the columns layout
            columns_layout.addLayout(left_column)
            columns_layout.addLayout(right_column)
            
            # Add columns layout to group layout
            group_layout.addLayout(columns_layout)
            
            self.system_checkboxes[category["id"]] = category_checkboxes
            group_box.setLayout(group_layout)
            self.systems_layout.addWidget(group_box)
        
        self.systems_layout.addStretch()
        scroll_area.setWidget(self.systems_container)
        right_layout.addWidget(scroll_area)
        
        return right_widget
        
    def on_tree_item_clicked(self, item, column):
        """Handle tree item click event"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
            
        # Clear all checkboxes first
        for category_checkboxes in self.system_checkboxes.values():
            for checkbox in category_checkboxes.values():
                checkbox.setChecked(False)
        
        # Load permissions for the selected item
        item_id = data["id"]
        item_type = data["type"]
        
        # If it's a position, load saved permissions from database
        if item_type == "position":
            dept_id = data.get('dept_id')
            position_id = item_id
            
            # Load permissions from database
            permissions = self.load_permissions_from_database(dept_id, position_id)
            
            # Apply permissions to checkboxes
            for category_id, systems in permissions.items():
                if category_id in self.system_checkboxes:
                    for system_id, is_enabled in systems.items():
                        if system_id in self.system_checkboxes[category_id]:
                            self.system_checkboxes[category_id][system_id].setChecked(is_enabled)
            
    def on_checkbox_changed(self, state):
        """Handle checkbox state change"""
        checkbox = self.sender()
        if checkbox:
            is_checked = state == Qt.Checked
            
            # Store the permission
            category_id = checkbox.category_id
            system_id = checkbox.system_id
            
            # Get current selected item
            current_item = self.tree_widget.currentItem()
            if current_item:
                item_data = current_item.data(0, Qt.UserRole)
                if item_data and item_data['type'] == 'position':
                    dept_id = item_data.get('dept_id')
                    position_id = item_data['id']
                    
                    # Save to database
                    self.save_permissions_to_database(dept_id, position_id, category_id, system_id, is_checked)
                    
                    # Also keep in-memory storage for compatibility
                    item_key = f"{item_data['type']}_{item_data['id']}"
                    if item_key not in self.access_permissions:
                        self.access_permissions[item_key] = {}
                    
                    if category_id not in self.access_permissions[item_key]:
                        self.access_permissions[item_key][category_id] = {}
                    
                    self.access_permissions[item_key][category_id][system_id] = is_checked
                
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
        
        # Access Matrix button (current screen)
        access_matrix_btn = QPushButton("Access Matrix")
        access_matrix_btn.setFixedHeight(40)  # Fixed height for buttons
        access_matrix_btn.setMinimumWidth(120)  # Minimum width
        access_matrix_btn.setStyleSheet("""
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
        access_matrix_btn.setEnabled(False)  # Disable since we're already on this screen
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
        departments_btn.clicked.connect(self.open_departments_and_positions)
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
    
    def open_departments_and_positions(self):
        """Open the departments and positions screen"""
        if DepartmentsAndPositionsScreen:
            self.departments_screen = DepartmentsAndPositionsScreen()
            self.departments_screen.show()
            self.hide()  # Hide the current screen
        else:
            QMessageBox.warning(self, "Error", "Departments and Positions screen is not available yet.")
    
    def run(self):
        """Start the main screen"""
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    main = MainScreen()
    main.run()
    sys.exit(app.exec_())