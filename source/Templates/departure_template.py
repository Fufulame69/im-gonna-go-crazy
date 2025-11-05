import fpdf

class SeparationChecklistPDF(fpdf.FPDF):
    """
    Custom PDF class to generate the Employee Separation Checklist.
    It recreates the structure from the provided image.
    """
    
    # Define colors (approximated from the image)
    HEADER_BLUE = (0, 176, 240)
    HEADER_TEXT = (255, 255, 255)
    BORDER_GRAY = (210, 210, 210)
    FIELD_HEIGHT = 7  # Height for single-line text fields
    CHECKBOX_SIZE = 4   # Size for checkboxes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(True, margin=15)
        self.set_margins(10, 10, 10)

    def draw_section_header(self, text, subtitle='', thicker=False):
        """Draws the main blue section headers."""
        self.set_fill_color(*self.HEADER_BLUE)
        self.set_text_color(*self.HEADER_TEXT)
        self.set_font('Helvetica', 'B', 10)
        
        # Calculate header height (thicker for observations)
        header_height = 10 if thicker else 8
        
        # Main title part - extend full width
        self.cell(0, header_height, f" {text}", border=0, ln=1, fill=True, align='L')
        
        # Subtitle part (if any)
        if subtitle:
            self.set_font('Helvetica', '', 8)
            self.cell(0, header_height, subtitle, border=0, ln=1, fill=True, align='L')
        
        self.set_text_color(0, 0, 0) # Reset text color
        self.ln(2) # Add a small gap

    def draw_main_title(self):
        """Draws the top 'Information Technologies' title."""
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 8, "Information Technologies", border=0, ln=1, align='C')
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 8, "Employee Separation Checklist", border=0, ln=1, align='C')
        self.ln(2)

    def draw_header_paragraph(self):
        """Draws the introductory paragraph."""
        self.set_font('Helvetica', '', 8)
        text = ("Management must process terminations promptly and ensure all terminated team members are terminated in PeopleSoft and their "
                "access removed or disabled from all other systems immediately (IE: within 14 days from the date of termination). Involuntary "
                "terminations should be processed immediately.")
        self.multi_cell(0, 4, text, border=0, align='L')
        self.ln(4)

    def draw_footer_paragraph(self):
        """Draws the final paragraph at the bottom."""
        self.set_font('Helvetica', '', 8)
        text = ("Any business emergencies requiring exceptions must be approved in writing and for a specified period of time by the Director of Finance (or "
                "designee) and copied to the regional finance representative. The documented approval must be maintained for subsequent audit verification.")
        self.multi_cell(0, 4, text, border=0, align='L')

    def draw_data_field(self, label, label_width, field_width, default_text=""):
        """Draws a label and a bordered 'textbox' cell."""
        self.set_font('Helvetica', 'B', 9)
        self.cell(label_width, self.FIELD_HEIGHT, label, border=0, align='L')
        self.set_font('Helvetica', '', 9)
        self.set_draw_color(*self.BORDER_GRAY)
        self.cell(field_width, self.FIELD_HEIGHT, f" {default_text}", border=1, align='L')

    def draw_checkbox_item(self, label):
        """Draws a checkbox and its label."""
        self.set_draw_color(0, 0, 0) # Black border for checkbox
        # Get Y to center text with box
        y_pos = self.get_y()
        self.rect(self.get_x() + 1, y_pos + (self.FIELD_HEIGHT - self.CHECKBOX_SIZE) / 2, self.CHECKBOX_SIZE, self.CHECKBOX_SIZE)
        self.set_x(self.get_x() + self.CHECKBOX_SIZE + 3) # Move past box
        self.set_font('Helvetica', '', 9)
        self.cell(0, self.FIELD_HEIGHT, label, border=0, ln=1, align='L')


    def generate_checklist(self, name="", onq_user="", department="", position="", date="", access_permissions=None, system_categories=None):
        """Main method to build the entire PDF document with employee data and access permissions."""
        if access_permissions is None:
            access_permissions = {}
        if system_categories is None:
            system_categories = []
            
        self.add_page()
        
        # === Main Title & Header ===
        self.draw_main_title()
        self.draw_header_paragraph()

        # === Employee Information ===
        self.draw_section_header("Employee Information:", " The form should be completed in its entirety and signed by the supervisor for processing.")
        
        # This section is a grid. We'll use fixed widths.
        # Page width is ~190mm (210 - 20 margins)
        label_w1 = 45
        field_w1 = 50
        label_w2 = 45
        field_w2 = 50 # 45+50+45+50 = 190

        # Row 1
        current_y = self.get_y()
        self.draw_data_field("Employee's Name", label_w1, field_w1, name)
        self.set_y(current_y)
        self.set_x(10 + label_w1 + field_w1) # Move to second column
        self.draw_data_field("Term / Separation Date", label_w2, field_w2, date if date else "Today's Date")
        self.ln(self.FIELD_HEIGHT + 1) # New line

        # Row 2
        current_y = self.get_y()
        self.draw_data_field("IDM User.", label_w1, field_w1, onq_user if onq_user else "0")
        self.set_y(current_y)
        self.set_x(10 + label_w1 + field_w1)
        self.draw_data_field("Hotel Name and Location", label_w2, field_w2, "Waldorf Astoria Punta Cacique")
        self.ln(self.FIELD_HEIGHT + 1)
        
        # Row 3
        current_y = self.get_y()
        self.draw_data_field("Employee's Position Title", label_w1, field_w1, position if position else "Asistente de Sistemas")
        self.set_y(current_y)
        self.set_x(10 + label_w1 + field_w1)
        self.draw_data_field("Manager's Name", label_w2, field_w2, "")
        self.ln(self.FIELD_HEIGHT + 1)
        current_y = self.get_y()
        self.draw_data_field("Manager's Phone", label_w1, field_w1, "+57 1 443 4400")
        self.set_y(current_y)
        self.set_x(10 + label_w1 + field_w1)
        self.draw_data_field("Manager's Signature", label_w2, field_w2, "")
        self.ln(self.FIELD_HEIGHT + 3) # Extra space after section
        
        # Row 4
        current_y = self.get_y()
        self.draw_data_field("Department Name", label_w1, field_w1, department if department else "")
        self.set_y(current_y)
        self.set_x(10 + label_w1 + field_w1)
        self.draw_data_field("Department Number", label_w2, field_w2, "0")
        self.ln(self.FIELD_HEIGHT + 1) # Consistent spacing with other rows

        # === Separation Information ===
        self.draw_section_header("Separation Information:", " List the date access should be removed and date processed.")
        self.draw_data_field("Date to Remove Access:", 45, 50, date if date else "")
        self.ln(self.FIELD_HEIGHT + 1)
        self.draw_data_field("Date to be Processed:", 45, 50, date if date else "")
        self.ln(self.FIELD_HEIGHT + 3)

        # === Network & Applications Access ===
        self.draw_section_header("Network & Applications Access:", " Mark the appropriate systems / access to be terminated. Note: ...")
        self.set_font('Helvetica', '', 8)
        self.multi_cell(0, 4, ("Note: Management must process terminations and ensure all current network and computer applications access and accounts are "
                               "terminated or removed immediately upon termination (IE: within 14 days). This includes PeopleSoft, OnQ Operations Audit, OnQ PMS, etc."),
                               border=0, align='L')
        self.ln(4)

        # --- Checkbox Section with Systems ---
        self.draw_systems_checkboxes(access_permissions, system_categories)

        # === Observations & Equipment ===
        obs_y = self.get_y()
        self.draw_section_header("Observations", "Equipment: Management must verify and securely obtain all company equipment prior to employee's termination date.", thicker=True)
        
        # Observations multi-cell on the left
        obs_width = 110
        self.set_draw_color(*self.BORDER_GRAY)
        self.multi_cell(obs_width, 30, "", border=1, align='L')
        obs_end_y = self.get_y()

        # Equipment section on the right - moved down 20 pixels
        equipment_y = obs_y + 20  # Position below the header with 20px spacing
        self.set_xy(10 + obs_width + 5, equipment_y)
        self.ln(2)
        
        # Equipment fields
        self.set_x(10 + obs_width + 5)
        self.draw_data_field("Laptop / Desktop:", 30, 45, "")
        self.ln(self.FIELD_HEIGHT + 1)
        self.set_x(10 + obs_width + 5)
        self.draw_data_field("Cell Phone:", 30, 45, "")
        self.ln(self.FIELD_HEIGHT + 1)
        self.set_x(10 + obs_width + 5)
        self.draw_data_field("Other:", 30, 45, "")
        
        # Set Y to below the taller of the two sections
        self.set_y(max(obs_end_y, self.get_y()) + 3)

        # === For IT / Management Use ===
        self.draw_section_header("For IT / Management Use:", " All completed forms must be signed and maintained for subsequent audit verification.")
        
        # Grid layout
        label_w = 60
        field_w = 65
        date_w = 20
        date_field_w = 15
        time_w = 10
        time_field_w = 15 # 60+65+20+15+10+15 = 185 (Close enough)

        # Row 1
        current_y = self.get_y()
        self.set_x(10)
        self.draw_data_field("Security access removed by:", label_w, field_w, "")
        self.set_y(current_y)
        self.set_x(10 + label_w + field_w)
        self.draw_data_field("Date:", date_w, date_field_w, "")
        self.set_y(current_y)
        self.set_x(10 + label_w + field_w + date_w + date_field_w)
        self.draw_data_field("Time:", time_w, time_field_w, "")
        self.ln(self.FIELD_HEIGHT + 1)

        # Row 2
        current_y = self.get_y()
        self.set_x(10)
        self.draw_data_field("Workstation collected or reassigned by:", label_w, field_w, "")
        self.set_y(current_y)
        self.set_x(10 + label_w + field_w)
        self.draw_data_field("Date:", date_w, date_field_w, "")
        self.set_y(current_y)
        self.set_x(10 + label_w + field_w + date_w + date_field_w)
        self.draw_data_field("Time:", time_w, time_field_w, "")
        self.ln(self.FIELD_HEIGHT + 3)
        
        # === Footer ===
        self.draw_footer_paragraph()
    
    def draw_systems_checkboxes(self, access_permissions, system_categories):
        """Draw systems as a compact list with hyphens"""
        # Collect all accessible systems
        accessible_systems = []
        
        for category in system_categories:
            category_id = category["id"]
            category_name = category["name"]
            
            # Get access permissions for this category
            category_access = access_permissions.get(category_id, {})
            
            # Get systems that have access permissions
            for system in category.get("systems", []):
                system_id = system["id"]
                system_name = system["name"]
                
                # Check if this system has access permission
                if category_access.get(system_id, False):
                    accessible_systems.append(system_name)
        
        # Set font for the systems list
        self.set_font('Helvetica', '', 9)
        
        # Start position
        start_x = self.get_x()
        start_y = self.get_y()
        current_x = start_x
        current_y = start_y
        line_height = 5  # Height of each line
        max_width = 190  # Maximum width of the line (page width minus margins)
        
        # Process each system
        for i, system_name in enumerate(accessible_systems):
            # Format the system name with hyphen
            system_text = f"-{system_name}"
            
            # Add space between systems (except for the first one)
            if i > 0:
                system_text = f" {system_text}"
            
            # Get the width of this text
            text_width = self.get_string_width(system_text)
            
            # Check if we need to move to the next line
            if current_x + text_width > start_x + max_width:
                # Move to next line
                current_x = start_x
                current_y += line_height
                # Remove the leading space for the first item on a new line
                system_text = system_text.lstrip()
                text_width = self.get_string_width(system_text)
            
            # Set position and write the text
            self.set_xy(current_x, current_y)
            self.cell(text_width, line_height, system_text, border=0, ln=0, align='L')
            
            # Update current x position
            current_x += text_width
        
        # Update the cursor position to below the systems list
        self.set_xy(start_x, current_y + line_height + 2)


# --- Main execution ---
if __name__ == "__main__":
    pdf = SeparationChecklistPDF(orientation='P', unit='mm', format='A4')
    pdf.generate_checklist()  # Uses default empty values for demo
    
    output_filename = "employee_separation_checklist.pdf"
    pdf.output(output_filename)
    print(f"Successfully generated {output_filename}")