import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QPushButton, QMessageBox,
                            QTreeWidget, QTreeWidgetItem, QScrollArea, QGroupBox,
                            QCheckBox, QSplitter, QFrame, QTableWidget, QTableWidgetItem,
                            QInputDialog, QComboBox, QDialog, QLineEdit, QTreeWidgetItemIterator)
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
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Departments
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Positions
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (40% left, 60% right)
        splitter.setSizes([480, 720])
        
        self.main_layout.addWidget(splitter)
        
        # Navigation bar
        self.create_navigation_bar()
    
    def create_left_panel(self):
        """Create the left panel with departments list"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        left_title = QLabel("Departments")
        left_title.setFont(QFont("Arial", 12, QFont.Bold))
        left_title.setStyleSheet("color: #2c3e50; padding: 5px;")
        left_layout.addWidget(left_title)
        
        # Tree widget for departments
        self.dept_tree_widget = QTreeWidget()
        self.dept_tree_widget.setHeaderLabels(["Department", "Actions"])
        self.dept_tree_widget.setColumnCount(2)
        self.dept_tree_widget.setColumnWidth(0, 300)  # Set width for department name column
        self.dept_tree_widget.setColumnWidth(1, 150)  # Set width for actions column
        self.dept_tree_widget.itemClicked.connect(self.on_department_clicked)
        
        # Populate tree with departments
        for dept in self.db_data.get("departments", []):
            dept_item = QTreeWidgetItem(self.dept_tree_widget)
            dept_item.setText(0, dept["name"])
            dept_item.setData(0, Qt.UserRole, {"id": dept["id"], "name": dept["name"]})
            
            # Create buttons for this department
            self.create_department_buttons(dept_item)
        
        left_layout.addWidget(self.dept_tree_widget)
        
        # Add department button
        add_dept_btn = QPushButton("Add Department")
        add_dept_btn.clicked.connect(self.add_department)
        left_layout.addWidget(add_dept_btn)
        
        return left_widget
    
    def create_right_panel(self):
        """Create the right panel with positions list"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        right_title = QLabel("Positions")
        right_title.setFont(QFont("Arial", 12, QFont.Bold))
        right_title.setStyleSheet("color: #2c3e50; padding: 5px;")
        right_layout.addWidget(right_title)
        
        # Tree widget for positions
        self.pos_tree_widget = QTreeWidget()
        self.pos_tree_widget.setHeaderLabels(["Position", "Actions"])
        self.pos_tree_widget.setColumnCount(2)
        self.pos_tree_widget.setColumnWidth(0, 300)  # Set width for position name column
        self.pos_tree_widget.setColumnWidth(1, 150)  # Set width for actions column
        self.pos_tree_widget.setEditTriggers(QTreeWidget.DoubleClicked | QTreeWidget.EditKeyPressed)
        
        # Connect signals for editing
        self.pos_tree_widget.itemChanged.connect(self.on_position_changed)
        self.pos_tree_widget.itemClicked.connect(self.store_original_position_value)
        
        # Flag to prevent showing message during initialization
        self.is_initialized = False
        
        # Store original values before editing
        self.original_position_values = {}
        
        right_layout.addWidget(self.pos_tree_widget)
        
        # Add position button
        add_pos_btn = QPushButton("Add Position")
        add_pos_btn.clicked.connect(self.add_position)
        right_layout.addWidget(add_pos_btn)
        
        # Set initialization flag to True after everything is set up
        self.is_initialized = True
        
        return right_widget
    
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
            from GUI.main_screen import MainScreen
            self.main_screen = MainScreen()
            self.main_screen.show()
            self.close()  # Close the current screen
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to import main screen: {str(e)}")
    
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
    
    
    def create_department_buttons(self, dept_item):
        """Create Edit and Delete buttons for a department item"""
        # Create a widget to hold the buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(2, 2, 2, 2)
        button_layout.setSpacing(5)
        
        # Create Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedSize(65, 30)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 9pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        # Create Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setFixedSize(65, 30)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 9pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        # Get department data
        dept_data = dept_item.data(0, Qt.UserRole)
        
        # Connect button signals
        edit_btn.clicked.connect(lambda checked, item=dept_item: self.edit_department(item))
        delete_btn.clicked.connect(lambda checked, item=dept_item: self.delete_department(item))
        
        # Add buttons to layout
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        
        # Set the widget as the item widget for column 1
        self.dept_tree_widget.setItemWidget(dept_item, 1, button_widget)
    
    def create_position_buttons(self, pos_item):
        """Create Edit and Delete buttons for a position item"""
        # Create a widget to hold the buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(2, 2, 2, 2)
        button_layout.setSpacing(5)
        
        # Create Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedSize(65, 30)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 9pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        # Create Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setFixedSize(65, 30)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 9pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        # Get position data
        pos_data = pos_item.data(0, Qt.UserRole)
        
        # Connect button signals
        edit_btn.clicked.connect(lambda checked, item=pos_item: self.edit_position(item))
        delete_btn.clicked.connect(lambda checked, item=pos_item: self.delete_position(item))
        
        # Add buttons to layout
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        
        # Set the widget as the item widget for column 1
        self.pos_tree_widget.setItemWidget(pos_item, 1, button_widget)
    
    def on_department_clicked(self, item, column):
        """Handle department click event for selection"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
            
        # Clear positions tree
        self.pos_tree_widget.clear()
        
        # Get department info
        dept_id = data["id"]
        dept_name = data["name"]
        
        # Find the department in the database
        for dept in self.db_data.get("departments", []):
            if dept.get("id") == dept_id:
                # Add positions to the right panel
                for position in dept.get("positions", []):
                    pos_item = QTreeWidgetItem(self.pos_tree_widget)
                    pos_item.setText(0, position["name"])
                    pos_item.setData(0, Qt.UserRole, {
                        "id": position["id"],
                        "name": position["name"],
                        "dept_id": dept_id,
                        "dept_name": dept_name
                    })
                    
                    # Create buttons for this position
                    self.create_position_buttons(pos_item)
                break
    
    def on_position_changed(self, item, column):
        """Handle position name change"""
        # Only process if the tree is fully initialized
        if hasattr(self, 'is_initialized') and self.is_initialized:
            new_value = item.text(0)
            data = item.data(0, Qt.UserRole)
            
            if data:
                original_name = data["name"]
                dept_id = data["dept_id"]
                pos_id = data["id"]
                
                if new_value != original_name:
                    # Update the database
                    if self.update_position_in_database(dept_id, pos_id, new_value):
                        # Update the stored data
                        data["name"] = new_value
                        item.setData(0, Qt.UserRole, data)
                        QMessageBox.information(self, "Success", "Position name updated successfully")
                    else:
                        # Revert the change if update failed
                        item.setText(0, original_name)
                        QMessageBox.warning(self, "Error", "Failed to update position name")
    
    def update_position_in_database(self, dept_id, pos_id, new_name):
        """Update position name in the database"""
        try:
            # Find the department in the database
            for dept in self.db_data.get("departments", []):
                if dept.get("id") == dept_id:
                    # Find the position within the department
                    for position in dept.get("positions", []):
                        if position.get("id") == pos_id:
                            # Update the position name
                            position["name"] = new_name
                            # Save the updated database
                            return self.save_database()
                    break
            return False
        except Exception as e:
            print(f"Error updating position in database: {str(e)}")
            return False
    
    def save_database(self):
        """Save the current database to file"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "database.json")
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(self.db_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving database: {str(e)}")
            return False
    
    
    def store_original_position_value(self, item, column):
        """Store the original position value before editing begins"""
        if hasattr(self, 'is_initialized') and self.is_initialized:
            data = item.data(0, Qt.UserRole)
            if data:
                self.original_position_values[data["id"]] = data["name"]
    
    def add_department(self):
        """Add a new department to the database"""
        # Get department name from user input
        dept_name, ok = QInputDialog.getText(self, "Add Department", "Enter department name:")
        
        if ok and dept_name.strip():
            # Generate a unique ID for the department
            dept_id = dept_name.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
            
            # Check if department already exists
            for dept in self.db_data.get("departments", []):
                if dept.get("name", "").lower() == dept_name.strip().lower():
                    QMessageBox.warning(self, "Error", f"Department '{dept_name}' already exists!")
                    return
            
            # Add new department to database
            new_department = {
                "id": dept_id,
                "name": dept_name.strip(),
                "positions": []
            }
            
            self.db_data["departments"].append(new_department)
            
            # Save the updated database
            if self.save_database():
                # Add the new department to the tree widget
                dept_item = QTreeWidgetItem(self.dept_tree_widget)
                dept_item.setText(0, dept_name.strip())
                dept_item.setData(0, Qt.UserRole, {"id": dept_id, "name": dept_name.strip()})
                
                # Create buttons for the new department
                self.create_department_buttons(dept_item)
                
                QMessageBox.information(self, "Success", f"Department '{dept_name}' added successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save changes to database")
    
    def add_position(self):
        """Add a new position to a department"""
        # Get the currently selected department
        current_dept_item = self.dept_tree_widget.currentItem()
        
        if not current_dept_item:
            QMessageBox.warning(self, "Error", "Please select a department first.")
            return
        
        dept_data = current_dept_item.data(0, Qt.UserRole)
        if not dept_data:
            QMessageBox.warning(self, "Error", "Invalid department selected.")
            return
        
        dept_id = dept_data["id"]
        dept_name = dept_data["name"]
        
        # Get position name from user input
        pos_name, ok = QInputDialog.getText(self, "Add Position", f"Enter position name for department '{dept_name}':")
        
        if ok and pos_name.strip():
            # Find the selected department in the database
            for dept in self.db_data.get("departments", []):
                if dept.get("id") == dept_id:
                    # Check if position already exists in this department
                    for pos in dept.get("positions", []):
                        if pos.get("name", "").lower() == pos_name.strip().lower():
                            QMessageBox.warning(self, "Error", f"Position '{pos_name}' already exists in department '{dept_name}'.")
                            return
                    
                    # Generate a unique ID for the position
                    pos_id = pos_name.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
                    
                    # Add new position to the department
                    new_position = {
                        "id": pos_id,
                        "name": pos_name.strip()
                    }
                    
                    dept["positions"].append(new_position)
                    
                    # Save the updated database
                    if self.save_database():
                        # Refresh the positions tree if this department is currently selected
                        if self.dept_tree_widget.currentItem() == current_dept_item:
                            self.on_department_clicked(current_dept_item, 0)
                        
                        QMessageBox.information(self, "Success", f"Position '{pos_name}' added to department '{dept_name}' successfully!")
                    else:
                        QMessageBox.critical(self, "Error", "Failed to save changes to database")
                    return
    
    def delete_department(self, item):
        """Delete a department after confirmation"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        dept_id = data["id"]
        dept_name = data["name"]
        
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the department '{dept_name}'?\n\nThis will also delete all positions within this department.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Find and remove the department from the database
            for i, dept in enumerate(self.db_data.get("departments", [])):
                if dept.get("id") == dept_id:
                    del self.db_data["departments"][i]
                    break
            
            # Save the updated database
            if self.save_database():
                # Remove the item from the tree widget
                root = self.dept_tree_widget.invisibleRootItem()
                root.removeChild(item)
                
                # Clear positions tree since the department is gone
                self.pos_tree_widget.clear()
                
                QMessageBox.information(self, "Success", f"Department '{dept_name}' deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save changes to database")
    
    def edit_department(self, item):
        """Edit a department name"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        dept_id = data["id"]
        old_name = data["name"]
        
        # Get new department name from user input
        new_name, ok = QInputDialog.getText(
            self,
            "Edit Department",
            "Enter new department name:",
            text=old_name
        )
        
        if ok and new_name.strip() and new_name.strip() != old_name:
            # Check if department name already exists
            for dept in self.db_data.get("departments", []):
                if dept.get("name", "").lower() == new_name.strip().lower() and dept.get("id") != dept_id:
                    QMessageBox.warning(self, "Error", f"Department '{new_name}' already exists!")
                    return
            
            # Update the department name in the database
            for dept in self.db_data.get("departments", []):
                if dept.get("id") == dept_id:
                    dept["name"] = new_name.strip()
                    break
            
            # Save the updated database
            if self.save_database():
                # Update the item in the tree widget
                item.setText(0, new_name.strip())
                data["name"] = new_name.strip()
                item.setData(0, Qt.UserRole, data)
                
                # Update positions that reference this department
                self.update_positions_dept_name(dept_id, new_name.strip())
                
                QMessageBox.information(self, "Success", f"Department name updated to '{new_name}' successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save changes to database")
    
    def update_positions_dept_name(self, dept_id, new_dept_name):
        """Update the department name in all positions that reference it"""
        for dept in self.db_data.get("departments", []):
            if dept.get("id") == dept_id:
                for position in dept.get("positions", []):
                    # Update positions tree if this department is currently selected
                    root = self.pos_tree_widget.invisibleRootItem()
                    for i in range(root.childCount()):
                        pos_item = root.child(i)
                        pos_data = pos_item.data(0, Qt.UserRole)
                        if pos_data and pos_data.get("dept_id") == dept_id:
                            pos_data["dept_name"] = new_dept_name
                            pos_item.setData(0, Qt.UserRole, pos_data)
                break
    
    def delete_position(self, item):
        """Delete a position after confirmation"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        dept_id = data["dept_id"]
        dept_name = data["dept_name"]
        pos_id = data["id"]
        pos_name = data["name"]
        
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the position '{pos_name}' from department '{dept_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Find the department and position in the database
            for dept in self.db_data.get("departments", []):
                if dept.get("id") == dept_id:
                    # Find and remove the position
                    for i, position in enumerate(dept.get("positions", [])):
                        if position.get("id") == pos_id:
                            del dept["positions"][i]
                            break
                    
                    # Save the updated database
                    if self.save_database():
                        # Remove the item from the tree widget
                        root = self.pos_tree_widget.invisibleRootItem()
                        root.removeChild(item)
                        
                        QMessageBox.information(self, "Success", f"Position '{pos_name}' deleted successfully!")
                    else:
                        QMessageBox.critical(self, "Error", "Failed to save changes to database")
                    return
    
    def edit_position(self, item):
        """Edit a position name"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        dept_id = data["dept_id"]
        dept_name = data["dept_name"]
        pos_id = data["id"]
        old_name = data["name"]
        
        # Get new position name from user input
        new_name, ok = QInputDialog.getText(
            self,
            "Edit Position",
            f"Enter new position name for department '{dept_name}':",
            text=old_name
        )
        
        if ok and new_name.strip() and new_name.strip() != old_name:
            # Check if position name already exists in this department
            for dept in self.db_data.get("departments", []):
                if dept.get("id") == dept_id:
                    for position in dept.get("positions", []):
                        if position.get("name", "").lower() == new_name.strip().lower() and position.get("id") != pos_id:
                            QMessageBox.warning(self, "Error", f"Position '{new_name}' already exists in department '{dept_name}'.")
                            return
                    break
            
            # Update the position name in the database
            if self.update_position_in_database(dept_id, pos_id, new_name.strip()):
                # Update the item in the tree widget
                item.setText(0, new_name.strip())
                data["name"] = new_name.strip()
                item.setData(0, Qt.UserRole, data)
                
                QMessageBox.information(self, "Success", f"Position name updated to '{new_name}' successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save changes to database")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    screen = DepartmentsAndPositionsScreen()
    screen.show()
    sys.exit(app.exec_())