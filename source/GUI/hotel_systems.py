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

# Import navigation bar and database manager
from GUI.navigation_bar import NavigationBar
from database.db_manager import db_manager

class HotelSystemsScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waldorf Access Form Generator - Hotel Systems")
        self.setGeometry(100, 100, 1200, 800)
        
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
        """Load data from the database using the database manager"""
        try:
            self.db_data = db_manager.load_database()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load database: {str(e)}")
            self.db_data = {"departments": [], "system_categories": [], "access_permissions": {}}
    
    def create_widgets(self):
        """Create all UI elements for the hotel systems screen"""
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - System Categories
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Systems
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (40% left, 60% right)
        splitter.setSizes([480, 720])
        
        self.main_layout.addWidget(splitter)
        
        # Navigation bar
        self.create_navigation_bar()
    
    def create_left_panel(self):
        """Create the left panel with system categories list"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        left_title = QLabel("System Categories")
        left_title.setFont(QFont("Arial", 12, QFont.Bold))
        left_title.setStyleSheet("color: #2c3e50; padding: 5px;")
        left_layout.addWidget(left_title)
        
        # Tree widget for system categories
        self.category_tree_widget = QTreeWidget()
        self.category_tree_widget.setHeaderLabels(["Category", "Actions"])
        self.category_tree_widget.setColumnCount(2)
        self.category_tree_widget.setColumnWidth(0, 300)  # Set width for category name column
        self.category_tree_widget.setColumnWidth(1, 150)  # Set width for actions column
        self.category_tree_widget.itemClicked.connect(self.on_category_clicked)
        
        # Populate tree with system categories
        for category in self.db_data.get("system_categories", []):
            category_item = QTreeWidgetItem(self.category_tree_widget)
            category_item.setText(0, category["name"])
            category_item.setData(0, Qt.UserRole, {"id": category["id"], "name": category["name"]})
            
            # Create buttons for this category
            self.create_category_buttons(category_item)
        
        left_layout.addWidget(self.category_tree_widget)
        
        # Add category button
        add_category_btn = QPushButton("Add Category")
        add_category_btn.clicked.connect(self.add_category)
        left_layout.addWidget(add_category_btn)
        
        return left_widget
    
    def create_right_panel(self):
        """Create the right panel with systems list"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        right_title = QLabel("Systems")
        right_title.setFont(QFont("Arial", 12, QFont.Bold))
        right_title.setStyleSheet("color: #2c3e50; padding: 5px;")
        right_layout.addWidget(right_title)
        
        # Tree widget for systems
        self.system_tree_widget = QTreeWidget()
        self.system_tree_widget.setHeaderLabels(["System", "Actions"])
        self.system_tree_widget.setColumnCount(2)
        self.system_tree_widget.setColumnWidth(0, 300)  # Set width for system name column
        self.system_tree_widget.setColumnWidth(1, 150)  # Set width for actions column
        self.system_tree_widget.setEditTriggers(QTreeWidget.DoubleClicked | QTreeWidget.EditKeyPressed)
        
        # Connect signals for editing
        self.system_tree_widget.itemChanged.connect(self.on_system_changed)
        self.system_tree_widget.itemClicked.connect(self.store_original_system_value)
        
        # Flag to prevent showing message during initialization
        self.is_initialized = False
        
        # Store original values before editing
        self.original_system_values = {}
        
        right_layout.addWidget(self.system_tree_widget)
        
        # Add system button
        add_system_btn = QPushButton("Add System")
        add_system_btn.clicked.connect(self.add_system)
        right_layout.addWidget(add_system_btn)
        
        # Set initialization flag to True after everything is set up
        self.is_initialized = True
        
        return right_widget
    
    def create_navigation_bar(self):
        """Create the navigation bar at the bottom of the screen"""
        nav_bar = NavigationBar(self, "hotel_systems")
        self.main_layout.addWidget(nav_bar)
    
    
    def create_category_buttons(self, category_item):
        """Create Edit and Delete buttons for a category item"""
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
        
        # Get category data
        category_data = category_item.data(0, Qt.UserRole)
        
        # Connect button signals
        edit_btn.clicked.connect(lambda checked, item=category_item: self.edit_category(item))
        delete_btn.clicked.connect(lambda checked, item=category_item: self.delete_category(item))
        
        # Add buttons to layout
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        
        # Set the widget as the item widget for column 1
        self.category_tree_widget.setItemWidget(category_item, 1, button_widget)
    
    def create_system_buttons(self, system_item):
        """Create Edit and Delete buttons for a system item"""
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
        
        # Get system data
        system_data = system_item.data(0, Qt.UserRole)
        
        # Connect button signals
        edit_btn.clicked.connect(lambda checked, item=system_item: self.edit_system(item))
        delete_btn.clicked.connect(lambda checked, item=system_item: self.delete_system(item))
        
        # Add buttons to layout
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        
        # Set the widget as the item widget for column 1
        self.system_tree_widget.setItemWidget(system_item, 1, button_widget)
    
    def on_category_clicked(self, item, column):
        """Handle category click event for selection"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
            
        # Clear systems tree
        self.system_tree_widget.clear()
        
        # Get category info
        category_id = data["id"]
        category_name = data["name"]
        
        # Find the category in the database
        for category in self.db_data.get("system_categories", []):
            if category.get("id") == category_id:
                # Add systems to the right panel
                for system in category.get("systems", []):
                    system_item = QTreeWidgetItem(self.system_tree_widget)
                    system_item.setText(0, system["name"])
                    system_item.setData(0, Qt.UserRole, {
                        "id": system["id"],
                        "name": system["name"],
                        "category_id": category_id,
                        "category_name": category_name
                    })
                    
                    # Create buttons for this system
                    self.create_system_buttons(system_item)
                break
    
    def on_system_changed(self, item, column):
        """Handle system name change"""
        # Only process if the tree is fully initialized
        if hasattr(self, 'is_initialized') and self.is_initialized:
            new_value = item.text(0)
            data = item.data(0, Qt.UserRole)
            
            if data:
                original_name = data["name"]
                category_id = data["category_id"]
                system_id = data["id"]
                
                if new_value != original_name:
                    # Update the database
                    if self.update_system_in_database(category_id, system_id, new_value):
                        # Update the stored data
                        data["name"] = new_value
                        item.setData(0, Qt.UserRole, data)
                        QMessageBox.information(self, "Success", "System name updated successfully")
                    else:
                        # Revert the change if update failed
                        item.setText(0, original_name)
                        QMessageBox.warning(self, "Error", "Failed to update system name")
    
    def update_system_in_database(self, category_id, system_id, new_name):
        """Update system name in the database"""
        try:
            # Find the category in the database
            for category in self.db_data.get("system_categories", []):
                if category.get("id") == category_id:
                    # Find the system within the category
                    for system in category.get("systems", []):
                        if system.get("id") == system_id:
                            # Update the system name
                            system["name"] = new_name
                            # Save the updated database
                            return self.save_database()
                    break
            return False
        except Exception as e:
            print(f"Error updating system in database: {str(e)}")
            return False
    
    def save_database(self):
        """Save the current database using the database manager"""
        try:
            return db_manager.save_database(self.db_data)
        except Exception as e:
            print(f"Error saving database: {str(e)}")
            return False
    
    
    def store_original_system_value(self, item, column):
        """Store the original system value before editing begins"""
        if hasattr(self, 'is_initialized') and self.is_initialized:
            data = item.data(0, Qt.UserRole)
            if data:
                self.original_system_values[data["id"]] = data["name"]
    
    def add_category(self):
        """Add a new category to the database"""
        # Get category name from user input
        category_name, ok = QInputDialog.getText(self, "Add Category", "Enter category name:")
        
        if ok and category_name.strip():
            # Generate a unique ID for the category
            category_id = category_name.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
            
            # Check if category already exists
            for category in self.db_data.get("system_categories", []):
                if category.get("name", "").lower() == category_name.strip().lower():
                    QMessageBox.warning(self, "Error", f"Category '{category_name}' already exists!")
                    return
            
            # Add new category to database
            new_category = {
                "id": category_id,
                "name": category_name.strip(),
                "systems": []
            }
            
            self.db_data["system_categories"].append(new_category)
            
            # Save the updated database
            if self.save_database():
                # Add the new category to the tree widget
                category_item = QTreeWidgetItem(self.category_tree_widget)
                category_item.setText(0, category_name.strip())
                category_item.setData(0, Qt.UserRole, {"id": category_id, "name": category_name.strip()})
                
                # Create buttons for the new category
                self.create_category_buttons(category_item)
                
                QMessageBox.information(self, "Success", f"Category '{category_name}' added successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save changes to database")
    
    def add_system(self):
        """Add a new system to a category"""
        # Get the currently selected category
        current_category_item = self.category_tree_widget.currentItem()
        
        if not current_category_item:
            QMessageBox.warning(self, "Error", "Please select a category first.")
            return
        
        category_data = current_category_item.data(0, Qt.UserRole)
        if not category_data:
            QMessageBox.warning(self, "Error", "Invalid category selected.")
            return
        
        category_id = category_data["id"]
        category_name = category_data["name"]
        
        # Get system name from user input
        system_name, ok = QInputDialog.getText(self, "Add System", f"Enter system name for category '{category_name}':")
        
        if ok and system_name.strip():
            # Find the selected category in the database
            for category in self.db_data.get("system_categories", []):
                if category.get("id") == category_id:
                    # Check if system already exists in this category
                    for system in category.get("systems", []):
                        if system.get("name", "").lower() == system_name.strip().lower():
                            QMessageBox.warning(self, "Error", f"System '{system_name}' already exists in category '{category_name}'.")
                            return
                    
                    # Generate a unique ID for the system
                    system_id = system_name.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
                    
                    # Add new system to the category
                    new_system = {
                        "id": system_id,
                        "name": system_name.strip()
                    }
                    
                    category["systems"].append(new_system)
                    
                    # Save the updated database
                    if self.save_database():
                        # Refresh the systems tree if this category is currently selected
                        if self.category_tree_widget.currentItem() == current_category_item:
                            self.on_category_clicked(current_category_item, 0)
                        
                        QMessageBox.information(self, "Success", f"System '{system_name}' added to category '{category_name}' successfully!")
                    else:
                        QMessageBox.critical(self, "Error", "Failed to save changes to database")
                    return
    
    def delete_category(self, item):
        """Delete a category after confirmation"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        category_id = data["id"]
        category_name = data["name"]
        
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the category '{category_name}'?\n\nThis will also delete all systems within this category.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Find and remove the category from the database
            for i, category in enumerate(self.db_data.get("system_categories", [])):
                if category.get("id") == category_id:
                    del self.db_data["system_categories"][i]
                    break
            
            # Save the updated database
            if self.save_database():
                # Remove the item from the tree widget
                root = self.category_tree_widget.invisibleRootItem()
                root.removeChild(item)
                
                # Clear systems tree since the category is gone
                self.system_tree_widget.clear()
                
                QMessageBox.information(self, "Success", f"Category '{category_name}' deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save changes to database")
    
    def edit_category(self, item):
        """Edit a category name"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        category_id = data["id"]
        old_name = data["name"]
        
        # Get new category name from user input
        new_name, ok = QInputDialog.getText(
            self,
            "Edit Category",
            "Enter new category name:",
            text=old_name
        )
        
        if ok and new_name.strip() and new_name.strip() != old_name:
            # Check if category name already exists
            for category in self.db_data.get("system_categories", []):
                if category.get("name", "").lower() == new_name.strip().lower() and category.get("id") != category_id:
                    QMessageBox.warning(self, "Error", f"Category '{new_name}' already exists!")
                    return
            
            # Update the category name in the database
            for category in self.db_data.get("system_categories", []):
                if category.get("id") == category_id:
                    category["name"] = new_name.strip()
                    break
            
            # Save the updated database
            if self.save_database():
                # Update the item in the tree widget
                item.setText(0, new_name.strip())
                data["name"] = new_name.strip()
                item.setData(0, Qt.UserRole, data)
                
                # Update systems that reference this category
                self.update_systems_category_name(category_id, new_name.strip())
                
                QMessageBox.information(self, "Success", f"Category name updated to '{new_name}' successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save changes to database")
    
    def update_systems_category_name(self, category_id, new_category_name):
        """Update the category name in all systems that reference it"""
        for category in self.db_data.get("system_categories", []):
            if category.get("id") == category_id:
                for system in category.get("systems", []):
                    # Update systems tree if this category is currently selected
                    root = self.system_tree_widget.invisibleRootItem()
                    for i in range(root.childCount()):
                        system_item = root.child(i)
                        system_data = system_item.data(0, Qt.UserRole)
                        if system_data and system_data.get("category_id") == category_id:
                            system_data["category_name"] = new_category_name
                            system_item.setData(0, Qt.UserRole, system_data)
                break
    
    def delete_system(self, item):
        """Delete a system after confirmation"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        category_id = data["category_id"]
        category_name = data["category_name"]
        system_id = data["id"]
        system_name = data["name"]
        
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the system '{system_name}' from category '{category_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Find the category and system in the database
            for category in self.db_data.get("system_categories", []):
                if category.get("id") == category_id:
                    # Find and remove the system
                    for i, system in enumerate(category.get("systems", [])):
                        if system.get("id") == system_id:
                            del category["systems"][i]
                            break
                    
                    # Save the updated database
                    if self.save_database():
                        # Remove the item from the tree widget
                        root = self.system_tree_widget.invisibleRootItem()
                        root.removeChild(item)
                        
                        QMessageBox.information(self, "Success", f"System '{system_name}' deleted successfully!")
                    else:
                        QMessageBox.critical(self, "Error", "Failed to save changes to database")
                    return
    
    def edit_system(self, item):
        """Edit a system name"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        category_id = data["category_id"]
        category_name = data["category_name"]
        system_id = data["id"]
        old_name = data["name"]
        
        # Get new system name from user input
        new_name, ok = QInputDialog.getText(
            self,
            "Edit System",
            f"Enter new system name for category '{category_name}':",
            text=old_name
        )
        
        if ok and new_name.strip() and new_name.strip() != old_name:
            # Check if system name already exists in this category
            for category in self.db_data.get("system_categories", []):
                if category.get("id") == category_id:
                    for system in category.get("systems", []):
                        if system.get("name", "").lower() == new_name.strip().lower() and system.get("id") != system_id:
                            QMessageBox.warning(self, "Error", f"System '{new_name}' already exists in category '{category_name}'.")
                            return
                    break
            
            # Update the system name in the database
            if self.update_system_in_database(category_id, system_id, new_name.strip()):
                # Update the item in the tree widget
                item.setText(0, new_name.strip())
                data["name"] = new_name.strip()
                item.setData(0, Qt.UserRole, data)
                
                QMessageBox.information(self, "Success", f"System name updated to '{new_name}' successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save changes to database")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    screen = HotelSystemsScreen()
    screen.show()
    sys.exit(app.exec_())