import datetime
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_font('Helvetica', '', 10)
        self.set_auto_page_break(auto=True, margin=15)
        self.form_cell_h = 7  # Height for input-like cells
        self.label_gap = 1    # Space between label and field
        self.section_gap = 4  # Space between form sections
        
        # Define colors (R, G, B)
        self.col_red_600 = (220, 38, 38)
        self.col_blue_900 = (30, 58, 138)
        self.col_gray_700 = (55, 65, 81)
        self.col_gray_500 = (107, 114, 128)
        self.col_gray_400 = (156, 163, 175)
        self.col_gray_300 = (209, 213, 219)
        self.col_gray_100 = (243, 244, 246)

    def draw_header(self, logo_path):
        """Draws the main page header."""
        try:
            # Logo - Adjust x, y, w, h as needed
            self.image(logo_path, x=10, y=10, w=40)
        except RuntimeError as e:
            print(f"Error loading logo: {e}. Displaying placeholder.")
            self.set_fill_color(*self.col_gray_100)
            self.set_draw_color(*self.col_gray_400)
            self.rect(10, 10, 40, 20, 'FD')
            self.set_xy(10, 15)
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(*self.col_gray_500)
            self.cell(40, 0, "Logo Patht", align='C')

        # --- Title Box ---
        box_x = 75
        box_y = 10
        box_w = 125 # Full width approx 210, margin 10. 210-20 = 190.
        
        # Border
        self.set_line_width(0.5)
        self.set_draw_color(*self.col_red_600)
        self.rect(box_x, box_y, box_w, 20) # Outer box

        # Content
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*self.col_red_600)
        self.set_xy(box_x, box_y + 3)
        self.cell(box_w, 0, "IT RISK CONTROL MATRIX - Sox Compliance", align='C')

        self.set_font('Helvetica', '', 7)
        self.set_text_color(*self.col_gray_500)
        self.set_xy(box_x, box_y + 8)
        self.cell(box_w, 0, "C10 - Access to critical systems and applications require user ID's and passwords.", align='C')

        self.set_xy(box_x, box_y + 11)
        self.cell(box_w, 0, "C10 - Acceso a sistemas y aplicaciones críticas requiere el uso de ID de usuario y password únicos.", align='C')

        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*self.col_blue_900)
        self.set_xy(box_x, box_y + 16)
        self.cell(box_w, 0, "Solicitud de Acceso a Sistemas - Departamento de Sistemas", align='C')
        
        # Reset colors and move down
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.ln(25) # Move down from top

    def draw_form_section(self):
        """Draws the main user information form fields."""
        
        # --- Row 1: Nombre, Posicion, Departamento, Fecha ---
        page_w = self.w - self.l_margin - self.r_margin
        col_w = page_w / 4 - 2 # 4 columns with 2mm gap
        
        # Store current Y position for text labels
        label_y = self.get_y()
        box_y = label_y + 6 # Position boxes below labels
        
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*self.col_gray_700)
        
        # Field 1: NOMBRE - Position text above where box will be
        self.set_xy(self.l_margin, label_y)
        self.cell(col_w, 5, "NOMBRE Y APELLIDO")
        
        # Field 2: POSICION
        self.set_xy(self.l_margin + col_w + 2, label_y)
        self.cell(col_w, 5, "POSICION")
        
        # Field 3: DEPARTAMENTO
        self.set_xy(self.l_margin + (col_w + 2) * 2, label_y)
        self.cell(col_w, 5, "DEPARTAMENTO")

        # Field 4: Fecha Ingreso
        self.set_xy(self.l_margin + (col_w + 2) * 3, label_y)
        self.cell(col_w, 5, "Fecha Ingreso")
        
        # Move to box position
        self.set_y(box_y)
        
        # --- Input boxes for Row 1 ---
        self.set_draw_color(*self.col_gray_400)
        self.set_font('Helvetica', '', 9)
        
        # Box 1 - Draw empty box first
        start_x = self.get_x()
        self.rect(start_x, self.get_y(), col_w, self.form_cell_h)
        self.set_x(start_x + col_w + 2) # Move to next position
        
        # Box 2 - Draw empty box first
        box2_x = self.get_x()
        self.rect(box2_x, self.get_y(), col_w, self.form_cell_h)
        self.set_x(start_x + (col_w + 2) * 2) # Move to next position
        
        # Box 3 - Draw empty box first
        box3_x = self.get_x()
        self.rect(box3_x, self.get_y(), col_w, self.form_cell_h)
        self.set_x(start_x + (col_w + 2) * 3) # Move to next position
        
        # Box 4 - Draw box with background
        box4_x = self.get_x()
        self.set_fill_color(*self.col_gray_100)
        self.rect(box4_x, self.get_y(), col_w, self.form_cell_h, 'F')
        
        # Add text on top of box 4
        today = datetime.date.today().strftime("%d-%b-%y")
        self.set_xy(box4_x + 1, self.get_y() + 1.5)
        self.cell(col_w - 2, self.form_cell_h - 2, today, align='C')
        self.set_fill_color(255, 255, 255) # Reset fill
        
        self.ln(self.form_cell_h + self.section_gap) # Move down

        # --- Row 2: IDM Login, Email ---
        col_w_2 = page_w / 2 - 1 # 2 columns with 2mm gap
        
        # Store positions for labels above boxes
        label_y = self.get_y()
        box_y = label_y + 6
        
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*self.col_gray_700)
        
        # Field 1: IDM Login - Position text above box
        self.set_xy(self.l_margin, label_y)
        self.cell(col_w_2, 5, "IDM Login Name")
        
        # Field 2: Email Account
        self.set_xy(self.l_margin + col_w_2 + 2, label_y)
        self.cell(col_w_2, 5, "Email Account")
        
        # Move to box position
        self.set_y(box_y)
        
        # --- Input boxes for Row 2 ---
        start_x = self.get_x()
        # Draw empty boxes first
        self.rect(start_x, self.get_y(), col_w_2, self.form_cell_h)
        box2_x = start_x + col_w_2 + 2
        self.rect(box2_x, self.get_y(), col_w_2, self.form_cell_h)
        
        # --- Sub-labels ---
        self.ln(self.form_cell_h + 1)
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*self.col_gray_500)
        self.cell(col_w_2, 5, "Solo para uso de computacion")
        
        self.ln(self.form_cell_h + self.section_gap) # Move down

    def draw_system_section(self, title, options):
        """Draws a bordered section for a system."""
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(*self.col_blue_900)
        self.set_text_color(255, 255, 255)
        
        # Header bar
        self.cell(0, 6, f"  {title.upper()}", fill=True, border=0, new_x="LMARGIN", new_y="NEXT")
        
        # Reset color
        self.set_text_color(0, 0, 0)
        
        # Section border
        self.set_draw_color(*self.col_gray_300)
        start_y = self.get_y()
        
        # Draw options
        self.set_font('Helvetica', '', 8)
        padding = 4
        self.set_x(self.get_x() + padding)
        
        # Calculate max columns
        max_cols = 4
        page_w = self.w - self.l_margin - self.r_margin - (2 * padding)
        col_w = page_w / max_cols
        
        y_pos = self.get_y() + 2 # Start Y for checkboxes
        
        for i, option in enumerate(options):
            col_index = i % max_cols
            if col_index == 0 and i > 0:
                y_pos += 5 # Move to next row
                
            x_pos = self.l_margin + padding + (col_w * col_index)
            self.set_xy(x_pos, y_pos)
            
            # Checkbox
            self.rect(x_pos, y_pos, 3, 3)
            # Label
            self.set_x(x_pos + 4)
            self.cell(col_w - 4, 3, option)

        # Move Y down
        self.set_y(y_pos + 5) # Move below the last row of checkboxes
        
        # Draw border around the content
        end_y = self.get_y()
        self.rect(self.l_margin, start_y, self.w - self.l_margin - self.r_margin, end_y - start_y)
        
        self.ln(self.section_gap)


    def draw_acknowledgement(self):
        """Draws the acknowledgement checkbox and text."""
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*self.col_gray_700)
        
        # Checkbox
        self.rect(self.l_margin, self.get_y(), 3.5, 3.5)
        
        # Text
        self.set_x(self.l_margin + 5)
        ack_text = "Yo, ____________________, he entendido y reconozco la responsabilidad de mi login name y password, así como también recibí y acepté el contenido de Las Políticas de seguridad de la información (HWI-IT-001)."
        self.multi_cell(0, 3.5, ack_text)
        
        self.ln(self.section_gap)

    def draw_observations(self):
        """Draws the observations box and device checkboxes."""
        # Position label above the textarea
        label_y = self.get_y()
        box_y = label_y + 6
        
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*self.col_gray_700)
        self.set_xy(self.l_margin, label_y)
        self.cell(0, 5, "Observaciones:")
        
        # Move to box position
        self.set_y(box_y)
        
        obs_w = self.w - self.l_margin - self.r_margin - 40 # Leave 40mm for checkboxes
        
        # Textarea
        self.set_draw_color(*self.col_gray_400)
        obs_y = self.get_y()
        self.rect(self.l_margin, obs_y, obs_w, 12)
        
        # --- Checkboxes ---
        self.set_font('Helvetica', '', 9)
        self.set_text_color(0, 0, 0)
        
        check_x = self.l_margin + obs_w + 5
        
        # Checkbox 1
        self.set_xy(check_x, self.get_y())
        self.rect(check_x, self.get_y(), 3.5, 3.5)
        self.set_x(check_x + 5)
        self.cell(0, 3.5, "Laptop / PC")
        
        # Checkbox 2
        self.ln(5)
        self.set_x(check_x)
        self.rect(check_x, self.get_y(), 3.5, 3.5)
        self.set_x(check_x + 5)
        self.cell(0, 3.5, "Celular")
        
        self.ln(10) # Move down past observations box

    def draw_footer_signatures(self):
        """Draws the 5-column signature block with improved text handling and spacing."""
        self.set_y(-55) # Position from bottom
        
        # Draw top border line
        self.set_draw_color(*self.col_gray_300)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

        page_w = self.w - self.l_margin - self.r_margin
        col_w = page_w / 5 - 4 # 5 columns with 4mm gap for more signing space
        start_y = self.get_y()
        
        titles = [
            "Usuario",
            "Solicitado por Lider\nDepartamento",
            "Aprobador por Recursos\nHumanos",
            "Aprobador por Finanzas",
            "Accesos Generados Por IT"
        ]
        
        # First pass: calculate the maximum title height
        max_title_height = 0
        for title in titles:
            # Calculate how many lines this title needs
            lines = title.count('\n') + 1
            title_height = lines * 4  # 4mm per line
            max_title_height = max(max_title_height, title_height)
        
        # Increase spacing between text and signature line for better signing space
        text_to_sig_spacing = 12  # Increased from 4 to 12mm for perfect signing space
        sig_y = start_y + max_title_height + text_to_sig_spacing
        
        for i, title in enumerate(titles):
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(*self.col_gray_700)
            
            x_pos = self.l_margin + (col_w + 4) * i  # Increased gap from 2 to 4mm
            self.set_xy(x_pos, start_y)
            
            # Title - use multi_cell to handle text wrapping and multiple lines
            self.multi_cell(col_w, 4, title, align='C')
            
            # Signature Line - use calculated sig_y for all columns
            self.set_draw_color(*self.col_gray_400)
            self.line(x_pos + 2, sig_y, x_pos + col_w - 2, sig_y)
            
            # Fecha label
            self.set_xy(x_pos, sig_y + 3)  # Increased spacing from 2 to 3mm
            self.set_font('Helvetica', '', 7)
            self.set_text_color(*self.col_gray_500)
            self.cell(col_w, 5, "Fecha", align='C')
            
            # Fecha input box - Draw empty box with increased spacing
            self.set_xy(x_pos + 2, sig_y + 8)  # Increased from 7 to 8mm
            self.set_draw_color(*self.col_gray_400)
            self.rect(x_pos + 2, sig_y + 8, col_w - 4, 5)


def create_solicitud_pdf():
    """Main function to create the PDF."""
    
    # --- IMPORTANT ---
    # 1. You must have fpdf2 installed: pip install fpdf2
    # 2. Download the 'Inter' font .ttf files and place them in a 'fonts' folder
    #    or change the font names in PDF.__init__ to a standard font like 'Helvetica'
    # 3. Update this logo_path to point to your actual logo file.
    
    logo_path = "assets/waldorf_logo.png" # <--- UPDATE THIS PATH
    
    # --- Mock data for dynamic sections (from HTML) ---
    # This data would come from your application logic
    sistema_base = {
        "title": "Sistema Base",
        "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4", "Opción 5"]
    }
    sistema_finanzas = {
        "title": "Finanzas",
        "options": ["Acceso Contabilidad", "Ver Reportes", "Aprobar Pagos", "Solo Lectura"]
    }

    try:
        # Create PDF object (Letter size, mm units)
        pdf = PDF(orientation='P', unit='mm', format='Letter')
        pdf.set_margins(10, 10, 10)
        pdf.add_page()
        
        # Draw the sections
        pdf.draw_header(logo_path)
        pdf.draw_form_section()
        
        # --- DYNAMIC_SYSTEM_SECTIONS_PLACEHOLDER ---
        # This is where you would loop through your system data
        # and call draw_system_section() for each one.
        pdf.draw_system_section(sistema_base["title"], sistema_base["options"])
        pdf.draw_system_section(sistema_finanzas["title"], sistema_finanzas["options"])
        # Add more calls as needed...
        
        pdf.draw_acknowledgement()
        pdf.draw_observations()
        pdf.draw_footer_signatures()

        # Save the PDF
        output_filename = "solicitud_de_acceso.pdf"
        pdf.output(output_filename)
        
        print(f"Successfully generated {output_filename}")

    except FileNotFoundError as e:
        if "Inter" in str(e):
            print("\n--- FONT ERROR ---")
            print("Could not find the 'Inter' font files.")
            print("Please download 'Inter-Regular.ttf' and 'Inter-Bold.ttf' from Google Fonts")
            print("and place them in a folder named 'fonts' in the same directory as this script.")
            print("Alternatively, change the font name in PDF.__init__ to 'Helvetica' or 'Arial'.")
        else:
            print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    create_solicitud_pdf()
