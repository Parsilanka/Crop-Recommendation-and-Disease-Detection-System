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

# Main Title (Clear, Concise, 10-20 words)
system_name = "Crop Doctor"
main_title = f"{system_name}: Enhancing Agricultural Decision-Making Among Small-Scale Farmers through AI-Driven Analytics"
elements.append(Paragraph("PROPOSED RESEARCH TITLE", heading_style))
elements.append(Paragraph(f"<b>\"{main_title}\"</b>", title_style))
elements.append(Spacer(1, 12))

# Section 1: Characteristics of the Title
elements.append(Paragraph("1. CHARACTERISTICS OF THE TITLE", heading_style))
characteristics = [
    "<b>Conciseness:</b> 14 words (within the 10-20 word recommended range).",
    "<b>Scope:</b> Focuses on decision-making enhancement in small-scale farming.",
    "<b>Variables:</b> AI-Driven Analytics (Independent) and Decision-Making (Dependent).",
    "<b>Clarity:</b> Avoids technical jargon to remain accessible to all stakeholders."
]
for char in characteristics:
    elements.append(Paragraph(f"• {char}", styles['BodyText']))
    elements.append(Spacer(1, 4))
elements.append(Spacer(1, 12))

# Section 2: Research Methodology
elements.append(Paragraph("2. RESEARCH METHODOLOGY", heading_style))

methodology_data = [
    ("Research Design", "A <b>Mixed-Method approach</b> combining quantitative system performance analytics with qualitative user experience interviews."),
    ("Research Locale", "The study is conducted within <b>sub-regions of Kenya</b>, focusing on areas with active small-scale cereal and vegetable production."),
    ("Population & Sampling", "<b>Small-scale farmers</b> (N=50) selected via <b>Purposive Sampling</b> based on smartphone literacy and active farming status."),
    ("Research Instrument", "<b>Automated Data Logs</b> for system accuracy and <b>Semi-Structured Questionnaires</b> for user impact assessment."),
    ("Data Collection", "A <b>three-phase process</b>: Pre-test baseline survey, 4-week system interaction period, and post-study performance review."),
    ("Data Analysis", "<b>Statistical Regression</b> for accuracy correlation and <b>Thematic Analysis</b> for qualitative feedback interpretation."),
    ("Ethical Considerations", "Strict adherence to <b>Informed Consent</b> protocols and <b>Confidentiality</b> of farmer location and yield data.")
]

for label, desc in methodology_data:
    elements.append(Paragraph(f"<b>{label}:</b> {desc}", styles['Justify']))
    elements.append(Spacer(1, 6))
elements.append(Spacer(1, 12))

# Section 3: Group Project Context
elements.append(Paragraph("3. GROUP PROJECT & COLLABORATION", heading_style))

group_data = [
    ("Division of Tasks", "Backend/AI development, Frontend UX design, Database architecture, and Documentation/Research writing."),
    ("Timeline", "<b>Total Duration: 12 Weeks</b> (Design: 3w, Implementation: 6w, Testing/Writing: 3w)."),
    ("Group Roles", "Project Leader, Lead Developer, Data Scientist, UX Designer, and Technical Writer."),
    ("Collaboration Tools", "<b>GitHub</b> for version control, <b>VSC</b> for development, and <b>Google Docs</b> for collaborative writing.")
]

for label, desc in group_data:
    elements.append(Paragraph(f"<b>{label}:</b> {desc}", styles['Justify']))
    elements.append(Spacer(1, 6))
elements.append(Spacer(1, 12))

# Section 4: System Identity
elements.append(Paragraph("4. SYSTEM OVERVIEW", heading_style))
elements.append(Paragraph(f"<b>System Name:</b> {system_name}", styles['BodyText']))
elements.append(Paragraph("<b>Core Capabilities:</b> Precision Crop Recommendation, Deep Learning Disease Isolation, and Expert Knowledge Exchange.", styles['BodyText']))

# Footer
elements.append(Spacer(1, 30))
footer_text = f"<i>Document Generated: {datetime.datetime.now().strftime('%B %d, %Y')}<br/>Research Proposal: {system_name} System</i>"
elements.append(Paragraph(footer_text, styles['Center']))

# Build PDF
doc.build(elements)
print(f"PDF generated successfully: {pdf_file}")
