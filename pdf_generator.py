from fpdf import FPDF
import os
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        # Logo
        # self.image('static/logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'Crop Disease Analysis Report', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} - Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

def generate_report(image_path, disease_name, confidence, details):
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Title Section
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(44, 62, 80) # Dark Blue
    pdf.cell(0, 10, f'Diagnosis: {disease_name}', 0, 1, 'L')
    
    # Confidence
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f'Confidence Level: {confidence}%', 0, 1, 'L')
    
    pdf.ln(5)
    
    # Image Section
    if os.path.exists(image_path):
        # Calculate aspect ratio to fit
        pdf.image(image_path, x=10, y=None, w=100)
    else:
        pdf.cell(0, 10, '[Image not found]', 0, 1)
        
    pdf.ln(10)
    
    # Details Section
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(236, 240, 241) # Light Gray
    pdf.cell(0, 10, 'Analysis Details', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    
    # Severity
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(30, 8, 'Severity:', 0, 0)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, str(details.get('severity', 'N/A')), 0, 1)
    
    # Treatment
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Recommended Treatment:', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, str(details.get('treatment', 'N/A')))
    pdf.ln(3)
    
    # Prevention
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Prevention Tips:', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, str(details.get('prevention', 'N/A')))
    
    # Save
    report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path = os.path.join("uploads", report_filename)
    pdf.output(output_path)
    
    return report_filename, output_path
