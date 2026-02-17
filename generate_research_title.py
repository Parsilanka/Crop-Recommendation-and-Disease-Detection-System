from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import datetime

# Create PDF
pdf_file = "Research_Title_Proposal.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=16,
    textColor='black',
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=12,
    textColor='black',
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

subheading_style = ParagraphStyle(
    'CustomSubHeading',
    parent=styles['Heading3'],
    fontSize=10,
    textColor='black',
    spaceAfter=6,
    fontName='Helvetica-Bold'
)

# Title
elements.append(Paragraph("RESEARCH TITLE PROPOSAL", title_style))
elements.append(Spacer(1, 12))

# Main Title
main_title = "An Intelligent Web-Based System for Precision Agriculture: Integrating Machine Learning for Crop Recommendation and Deep Learning for Plant Disease Detection with Real-Time Weather Analysis"
elements.append(Paragraph(main_title, heading_style))
elements.append(Spacer(1, 12))

# Subtitle
subtitle = "<i>A Comprehensive AI-Driven Platform for Sustainable Farming Through Data-Driven Crop Selection and Automated Disease Diagnosis</i>"
elements.append(Paragraph(subtitle, styles['Center']))
elements.append(Spacer(1, 20))

# Section 1: Research Title Structure
elements.append(Paragraph("1. RESEARCH TITLE STRUCTURE", heading_style))

elements.append(Paragraph("<b>1.1 Subject Area:</b>", subheading_style))
elements.append(Paragraph("Agricultural Technology, Precision Agriculture, Artificial Intelligence in Agriculture, Smart Farming Systems", styles['BodyText']))
elements.append(Spacer(1, 8))

elements.append(Paragraph("<b>1.2 Research Problem:</b>", subheading_style))
elements.append(Paragraph("Farmers face challenges in making optimal crop selection decisions and identifying plant diseases early, leading to reduced yields and economic losses. Traditional methods are time-consuming, require expert knowledge, and lack integration with environmental factors.", styles['Justify']))
elements.append(Spacer(1, 8))

elements.append(Paragraph("<b>1.3 Methodology/Approach:</b>", subheading_style))
elements.append(Paragraph("Machine Learning (Random Forest Classification), Deep Learning (Convolutional Neural Networks), Web Application Development (Flask Framework), Real-Time API Integration (Weather Data), Computer Vision (Image Processing)", styles['Justify']))
elements.append(Spacer(1, 8))

elements.append(Paragraph("<b>1.4 Scope/Population:</b>", subheading_style))
elements.append(Paragraph("Small to medium-scale farmers, agricultural extension officers, and farming communities seeking data-driven decision support for crop management and disease control.", styles['Justify']))
elements.append(Spacer(1, 8))

elements.append(Paragraph("<b>1.5 Expected Outcome:</b>", subheading_style))
elements.append(Paragraph("An accessible, intelligent system that provides accurate crop recommendations based on soil and climate parameters, identifies plant diseases with high precision, and offers actionable treatment recommendations, ultimately improving agricultural productivity and sustainability.", styles['Justify']))
elements.append(Spacer(1, 16))

# Section 2: Key Features
elements.append(Paragraph("2. SYSTEM KEY FEATURES", heading_style))

features = [
    "Soil-Based Crop Recommendation: ML model analyzes NPK levels, pH, temperature, humidity, and rainfall",
    "Disease Detection: Deep learning model (38 plant disease classes) with 95%+ accuracy",
    "Real-Time Weather Integration: Location-based weather data for informed decision-making",
    "Analysis History: Complete record of all disease diagnoses with timestamps",
    "PDF Report Generation: Downloadable treatment and prevention reports",
    "User-Friendly Interface: Responsive web design accessible on multiple devices",
    "Fallback Mechanisms: Color-based analysis when ML model unavailable"
]

for i, feature in enumerate(features, 1):
    elements.append(Paragraph(f"{i}. {feature}", styles['BodyText']))
    elements.append(Spacer(1, 4))

elements.append(Spacer(1, 12))

# Section 3: Technical Specifications
elements.append(Paragraph("3. TECHNICAL SPECIFICATIONS", heading_style))

elements.append(Paragraph("<b>3.1 Technologies Used:</b>", subheading_style))

tech_stack = [
    "Backend: Python 3.11, Flask Framework",
    "Machine Learning: Scikit-learn (Random Forest)",
    "Deep Learning: TensorFlow/Keras (CNN)",
    "Image Processing: PIL, NumPy",
    "Database: SQLite",
    "APIs: Open-Meteo (Weather), BigDataCloud (Geolocation)",
    "Report Generation: FPDF2",
    "Frontend: HTML5, CSS3, JavaScript"
]

for tech in tech_stack:
    elements.append(Paragraph(f"• {tech}", styles['BodyText']))

elements.append(Spacer(1, 8))

elements.append(Paragraph("<b>3.2 Dataset:</b>", subheading_style))
elements.append(Paragraph("PlantVillage Dataset (38 disease classes), Crop Recommendation Dataset (22 crops with soil/climate parameters)", styles['BodyText']))
elements.append(Spacer(1, 16))

# Section 4: Research Significance
elements.append(Paragraph("4. RESEARCH SIGNIFICANCE", heading_style))

significance = [
    "Addresses food security challenges through improved crop yields",
    "Reduces economic losses from crop diseases through early detection",
    "Democratizes agricultural expertise via accessible technology",
    "Promotes sustainable farming practices through data-driven decisions",
    "Contributes to digital agriculture transformation in developing regions",
    "Provides scalable solution adaptable to various geographical contexts"
]

for i, sig in enumerate(significance, 1):
    elements.append(Paragraph(f"{i}. {sig}", styles['BodyText']))
    elements.append(Spacer(1, 4))

elements.append(Spacer(1, 12))

# Section 5: Keywords
elements.append(Paragraph("5. KEYWORDS", heading_style))
keywords = "Precision Agriculture, Machine Learning, Deep Learning, Crop Recommendation, Plant Disease Detection, Computer Vision, Smart Farming, Agricultural Decision Support System, Convolutional Neural Networks, Web-Based Application, Sustainable Agriculture"
elements.append(Paragraph(keywords, styles['Justify']))
elements.append(Spacer(1, 16))

# Section 6: Alternative Titles
elements.append(Paragraph("6. ALTERNATIVE RESEARCH TITLES", heading_style))

alt_titles = [
    ("Alternative 1:", "Development of an AI-Powered Agricultural Advisory System for Crop Selection and Disease Management"),
    ("Alternative 2:", "Machine Learning and Deep Learning Approaches to Intelligent Crop Recommendation and Plant Pathology Detection"),
    ("Alternative 3:", "A Smart Farming Platform: Integrating Predictive Analytics for Crop Planning and Automated Disease Diagnosis"),
    ("Alternative 4:", "Web-Based Decision Support System for Precision Agriculture Using Artificial Intelligence and Real-Time Environmental Data")
]

for label, title in alt_titles:
    elements.append(Paragraph(f"<b>{label}</b>", styles['BodyText']))
    elements.append(Paragraph(title, styles['Justify']))
    elements.append(Spacer(1, 8))

# Footer
elements.append(Spacer(1, 20))
footer_text = f"<i>Document Generated: {datetime.datetime.now().strftime('%B %d, %Y')}<br/>Crop Recommendation and Disease Detection System</i>"
elements.append(Paragraph(footer_text, styles['Center']))

# Build PDF
doc.build(elements)
print(f"PDF generated successfully: {pdf_file}")
