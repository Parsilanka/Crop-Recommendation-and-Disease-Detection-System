"""
CropDoctor System Documentation PDF Generator
Generates a comprehensive PDF covering system overview, tools, database queries,
registered users, and probable exam/interview questions.

Run: python generate_system_doc.py
Output: CropDoctor_System_Documentation.pdf
"""
from fpdf import FPDF
from datetime import datetime
import os

# ---------------------------------------------------------------------------
# Unicode -> latin-1 sanitiser (fpdf2 core fonts only support latin-1)
# ---------------------------------------------------------------------------
_UNI_MAP = {
    '\u2013': '-',
    '\u2014': '--',
    '\u2018': "'",
    '\u2019': "'",
    '\u201c': '"',
    '\u201d': '"',
    '\u2022': '-',
    '\u2026': '...',
    '\u00a0': ' ',
    '\u2192': '->',   # arrow right
    '\u00b0': 'deg',  # degree
    '\u00d7': 'x',    # multiply
}

def S(text):
    """Return text safe for fpdf2 core fonts (latin-1 only)."""
    if not isinstance(text, str):
        text = str(text)
    for src, dst in _UNI_MAP.items():
        text = text.replace(src, dst)
    return text.encode('latin-1', errors='replace').decode('latin-1')


# ---------------------------------------------------------------------------
# PDF class
# ---------------------------------------------------------------------------
class Doc(FPDF):
    GREEN  = (34,  85,  34)
    BLUE   = (0,   60, 120)
    GREY   = (80,  80,  80)
    WHITE  = (255, 255, 255)
    BLACK  = (0,   0,   0)
    LGREY  = (240, 240, 240)
    LGREEN = (214, 234, 212)

    def header(self):
        self.set_fill_color(*self.GREEN)
        self.rect(0, 0, 210, 20, 'F')
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*self.WHITE)
        self.set_xy(0, 5)
        self.cell(0, 10,
                  S('CropDoctor  -  Crop Recommendation & Plant Disease Detection System'),
                  border=0, align='C')
        self.set_text_color(*self.BLACK)
        self.ln(18)

    def footer(self):
        self.set_y(-13)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(*self.GREY)
        ts = datetime.now().strftime('%d %B %Y, %H:%M')
        self.cell(0, 8,
                  S(f'Page {self.page_no()}/{{nb}}   |   Generated: {ts}   |   Group 3 - MUST'),
                  border=0, align='C')
        self.set_text_color(*self.BLACK)

    # ---- helpers -----------------------------------------------------------
    def hdr(self, title, r=34, g=85, b=34):
        self.ln(3)
        self.set_fill_color(r, g, b)
        self.set_text_color(*self.WHITE)
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 9, S('  ' + title), 0, 1, 'L', fill=True)
        self.set_text_color(*self.BLACK)
        self.ln(2)

    def sub(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*self.GREEN)
        self.cell(0, 7, S(title), 0, 1)
        self.set_text_color(*self.BLACK)

    def para(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 6, S(text))
        self.ln(1)

    def bul(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_x(self.l_margin + 8)
        self.multi_cell(self.epw - 8, 6, S('>> ' + text))

    def num(self, n, text):
        self.set_font('Helvetica', '', 10)
        self.set_x(self.l_margin + 8)
        self.multi_cell(self.epw - 8, 6, S(f'{n}. {text}'))

    def kv(self, key, val, kw=52):
        self.set_font('Helvetica', 'B', 10)
        self.cell(kw, 7, S(key + ':'), border=0)
        self.set_font('Helvetica', '', 10)
        self.multi_cell(self.epw - kw, 7, S(val))

    def code(self, text):
        self.set_fill_color(*self.LGREY)
        self.set_font('Courier', '', 8)
        self.set_text_color(30, 30, 100)
        self.multi_cell(0, 5.5, S(text), border=0, align='L', fill=True)
        self.set_text_color(*self.BLACK)
        self.ln(2)

    def qa(self, n, question, hint=None):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*self.BLUE)
        self.multi_cell(0, 6, S(f'Q{n}. {question}'))
        self.set_text_color(*self.BLACK)
        if hint:
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(60, 60, 60)
            self.set_x(self.l_margin + 8)
            self.multi_cell(self.epw - 8, 5.5, S('Answer Hint: ' + hint))
            self.set_text_color(*self.BLACK)
        self.ln(2)

    def line_sep(self):
        self.set_draw_color(180, 210, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def tbl_hdr(self, cols):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(*self.LGREEN)
        for txt, w in cols:
            self.cell(w, 8, S(txt), border=1, align='C', fill=True)
        self.ln()

    def tbl_row(self, vals_widths, fill=False):
        self.set_font('Helvetica', '', 9)
        fc = (245, 250, 245) if fill else (255, 255, 255)
        self.set_fill_color(*fc)
        for txt, w in vals_widths:
            self.cell(w, 7, S(str(txt)), border=1, fill=True)
        self.ln()


# ---------------------------------------------------------------------------
# Content helpers
# ---------------------------------------------------------------------------
def cover(pdf):
    pdf.add_page()
    logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'must_logo.png')
    if os.path.exists(logo):
        pdf.image(logo, x=80, y=28, w=50)
        pdf.ln(58)
    else:
        pdf.ln(22)

    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(34, 85, 34)
    pdf.cell(0, 12, 'CROPDOCTOR SYSTEM', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 9, 'Crop Recommendation & Plant Disease Detection', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)
    pdf.set_fill_color(34, 85, 34)
    pdf.rect(30, pdf.get_y(), 150, 1, 'F')
    pdf.ln(8)

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(40, 40, 40)
    for line in [
        'System Documentation, Database Query Guide',
        'Registered User Access & Probable Interview / Exam Questions',
        '',
        'Group 3  |  Meru University of Science & Technology (MUST)',
        'Generated: ' + datetime.now().strftime('%d %B %Y'),
    ]:
        pdf.cell(0, 8, S(line), align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(34, 85, 34)
    pdf.cell(0, 8, 'TABLE OF CONTENTS', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 10)
    toc = [
        ('1.', 'System Overview'),
        ('2.', 'Technology Stack & Tools'),
        ('3.', 'System Architecture'),
        ('4.', 'Database Schema & Models'),
        ('5.', 'How to Query the Database'),
        ('6.', 'How to View Registered Users'),
        ('7.', 'API Endpoints Reference'),
        ('8.', 'Machine Learning Models'),
        ('9.', 'Community & Expert Features'),
        ('10.', 'Probable Interview / Exam Questions (50+ Q&A)'),
        ('11.', 'Quick Reference Card'),
    ]
    for num, title in toc:
        pdf.cell(18, 7, S(num), border=0)
        pdf.cell(0, 7, S(title), border=0, new_x='LMARGIN', new_y='NEXT')


def system_overview(pdf):
    pdf.add_page()
    pdf.hdr('1. SYSTEM OVERVIEW')
    pdf.para(
        'CropDoctor is an intelligent, web-based agricultural decision-support platform developed '
        'by Group 3 at Meru University of Science and Technology (MUST). The system combines '
        'machine learning, image processing, and community-engagement features to help farmers '
        'make data-driven decisions on crop selection and plant disease management.\n\n'
        'The platform serves three core needs:'
    )
    pdf.bul('Crop Recommendation - predicts the best crop to plant based on soil nutrients (N, P, K), '
            'temperature, humidity, pH and rainfall using a trained Random Forest classifier.')
    pdf.bul('Plant Disease Detection - analyses uploaded leaf/plant photos and identifies diseases '
            'across 38 PlantVillage classes using a TensorFlow CNN model (with colour-heuristic fallback).')
    pdf.bul('Community Hub - provides forum discussions, expert consultations, reputation/gamification, '
            'and weather data integration for farmers.')

    pdf.ln(3)
    pdf.sub('Target Users')
    for u in ['Smallholder and commercial farmers', 'Agricultural extension officers',
               'Agronomists and plant pathologists (registered as experts)', 'System administrators']:
        pdf.bul(u)

    pdf.ln(3)
    pdf.sub('Key System Features')
    features = [
        ('Crop Recommendation Engine', 'Random Forest ML model trained on 2,200+ data points covering 22 crop classes'),
        ('Disease Detection', '38-class CNN (TensorFlow/Keras) + enhanced colour/pattern heuristic fallback'),
        ('Fertilizer Recommendations', 'Per-crop NPK ratios, application rates, organic alternatives & micronutrients'),
        ('PDF Report Generation', 'FPDF2-based downloadable disease analysis reports'),
        ('User Authentication', 'Flask-Login with Werkzeug hashed passwords, role-based access'),
        ('Forum System', 'Category-based posts, nested comments, upvotes/downvotes, flags, solved status'),
        ('Expert Consultation', 'Booking system with scheduling, video/phone/chat/in-person modes'),
        ('Reputation System', 'Gamified points and badges for user engagement'),
        ('Weather Integration', 'Live weather data via external API for planting guidance'),
        ('Notification System', 'In-app alerts for comments, bookings, upvotes'),
    ]
    for name, desc in features:
        pdf.kv(name, desc, kw=65)


def tech_stack(pdf):
    pdf.add_page()
    pdf.hdr('2. TECHNOLOGY STACK & TOOLS')

    categories = {
        'Backend Framework': [
            ('Flask 3.0.3', 'Micro web framework for routing, request handling, and templating'),
            ('Flask-Login 0.6.3', 'Session-based user authentication management'),
            ('Flask-SQLAlchemy 3.1.1', 'ORM layer for SQLite database interaction'),
            ('Flask-WTF 1.2.1', 'CSRF-protected form handling'),
            ('Flask-CORS 4.0.0', 'Cross-Origin Resource Sharing for API endpoints'),
            ('Flask-Mail 0.9.1', 'Email sending capabilities'),
        ],
        'Machine Learning & Data': [
            ('TensorFlow / Keras', 'Deep learning CNN model for plant disease classification (38 classes)'),
            ('scikit-learn 1.5.2', 'Random Forest crop recommendation; LabelEncoder, scalers'),
            ('NumPy 2.1.0', 'Numerical array operations for image preprocessing & feature engineering'),
            ('Pandas 2.2.3', 'Data loading, CSV processing (Crop_recommendation.csv, 2,200 rows)'),
            ('Pillow 10.2.0', 'Image loading, resizing (224x224), RGB conversion for ML pipeline'),
            ('pickle', 'Serialisation of trained crop model, label encoder, and scalers'),
        ],
        'Database': [
            ('SQLite', 'Relational database (community.db); zero-config file-based DB'),
            ('SQLAlchemy ORM', 'Declarative models; relationships, foreign keys, indexes'),
            ('python-dotenv 1.0.0', 'Environment variable management (.env for secrets/DB URIs)'),
        ],
        'Security & Auth': [
            ('Werkzeug', 'Password hashing via generate_password_hash / check_password_hash (PBKDF2)'),
            ('bcrypt 4.1.2', 'Additional hashing library'),
            ('bleach 6.1.0', 'HTML sanitisation to prevent XSS in forum posts'),
        ],
        'PDF & Reporting': [
            ('fpdf2 2.7.9', 'Pure-Python PDF generation for disease analysis reports'),
        ],
        'Utilities': [
            ('requests 2.32.3', 'HTTP calls for weather API and external integrations'),
            ('markdown 3.5.1', 'Markdown-to-HTML rendering for forum posts'),
            ('pytz 2024.1', 'Timezone-aware datetime handling'),
            ('kagglehub', 'Automated download of PlantVillage dataset from Kaggle'),
        ],
        'Frontend': [
            ('HTML5 / Jinja2 Templates', 'Server-side rendered pages in the templates/ directory'),
            ('Vanilla CSS', 'Styling without heavy CSS frameworks'),
            ('JavaScript (Fetch API)', 'Async calls to Flask JSON endpoints for crop/disease analysis'),
        ],
    }
    for cat, items in categories.items():
        pdf.sub(cat)
        for tool, desc in items:
            pdf.kv(tool, desc, kw=60)
        pdf.ln(2)


def architecture(pdf):
    pdf.add_page()
    pdf.hdr('3. SYSTEM ARCHITECTURE')
    pdf.para(
        'The application follows a monolithic MVC-style architecture. '
        'Two primary Flask application files handle different subsystems:'
    )
    pdf.sub('Core Files & Their Roles')
    files = [
        ('app.py (1,253 lines)', 'Main app - crop recommendation, disease detection, PDF reports, weather'),
        ('app_community.py', 'Community routes - login, register, logout, profile'),
        ('community_models.py', 'All SQLAlchemy ORM models (User, Forum, Expert, Booking, Reputation...)'),
        ('database_setup.py', 'DB initialisation, table creation, seeding admin/sample users'),
        ('expert_api.py', 'REST endpoints for expert consultation booking and management'),
        ('forum_api.py', 'REST endpoints for forum posts, comments, votes, flags'),
        ('history.py', 'Analysis history logging helpers'),
        ('weather.py', 'Weather API integration module'),
        ('pdf_generator.py', 'Disease report PDF generation using fpdf2'),
        ('train_crop_model.py', 'Script to train and save crop recommendation Random Forest model'),
        ('models/', 'Folder: plant_disease_model.h5, crop_recommendation_model.pkl, label_encoder.pkl'),
        ('templates/', 'Jinja2 HTML templates (11 files) for all web pages'),
        ('uploads/', 'User-uploaded plant images and generated PDF reports'),
        ('instance/', 'SQLite database files (community.db)'),
    ]
    for name, role in files:
        pdf.kv(name, role, kw=62)

    pdf.ln(3)
    pdf.sub('Request Flow (step by step)')
    steps = [
        'Browser sends HTTP request to Flask (app.py or app_community.py)',
        'Flask-Login checks session / authentication status',
        'Route handler processes request (calls ML model or DB query)',
        'Crop Recommendation: form input -> normalise features -> crop_model.predict() -> return top-N crops',
        'Disease Detection: save image -> preprocess_image_for_ml() -> model.predict() (or fallback)',
        'Result rendered via Jinja2 template or returned as JSON to browser JavaScript',
        'User optionally downloads a PDF report generated by pdf_generator.py',
    ]
    for i, s in enumerate(steps, 1):
        pdf.num(i, s)


def db_schema(pdf):
    pdf.add_page()
    pdf.hdr('4. DATABASE SCHEMA & MODELS')
    pdf.para('The SQLite database (instance/community.db) contains 15+ tables managed by SQLAlchemy ORM.')

    tables = [
        ('users', 'id, username, email, password_hash, full_name, location, phone, reputation_points, is_expert, is_admin, is_verified, created_at, last_login'),
        ('user_profiles', 'id, user_id(FK), bio, avatar_url, expertise_areas, farm_size, crops_grown, languages'),
        ('forum_categories', 'id, name, description, icon, slug, post_count'),
        ('forum_posts', 'id, title, content, author_id(FK), category_id(FK), location, tags, views, is_solved, is_pinned, created_at'),
        ('forum_comments', 'id, content, post_id(FK), author_id(FK), parent_comment_id(FK), is_best_answer, created_at'),
        ('post_votes', 'id, post_id(FK), user_id(FK), vote_type [upvote/downvote], created_at'),
        ('comment_votes', 'id, comment_id(FK), user_id(FK), vote_type, created_at'),
        ('post_flags', 'id, post_id(FK), user_id(FK), reason, status [pending/resolved], created_at'),
        ('expert_profiles', 'id, user_id(FK), specializations, credentials, bio, hourly_rate, years_experience, is_verified, is_available, average_rating'),
        ('expert_availability', 'id, expert_id(FK), day_of_week [0-6], start_time, end_time, is_active'),
        ('consultation_bookings', 'id, expert_id(FK), farmer_id(FK), booking_date, mode, status, crop_type, urgency, payment_status, payment_amount'),
        ('consultation_reviews', 'id, booking_id(FK), rating [1-5], review_text, would_recommend, created_at'),
        ('expert_badges / user_badges', 'id, expert_id/user_id(FK), badge_type, badge_name, description, awarded_at'),
        ('reputation_logs', 'id, user_id(FK), points, action_type, reference_id, created_at'),
        ('notifications', 'id, user_id(FK), title, message, notification_type, is_read, created_at'),
    ]

    pdf.tbl_hdr([('Table Name', 46), ('Key Columns', 0)])
    for i, (tbl, cols) in enumerate(tables):
        pdf.tbl_row([(tbl, 46), (cols, 0)], fill=(i % 2 == 0))


def db_queries(pdf):
    pdf.add_page()
    pdf.hdr('5. HOW TO QUERY THE DATABASE')

    pdf.sub('Method A: Python / SQLAlchemy ORM (inside Flask app context)')
    pdf.code("""\
from flask import Flask
from community_models import db, User, ForumPost, ExpertProfile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/community.db'
app.config['SECRET_KEY'] = 'dev'
db.init_app(app)

with app.app_context():
    # All registered users
    users = User.query.all()
    for u in users:
        print(u.id, u.username, u.email, u.created_at)

    # Only experts
    experts = User.query.filter_by(is_expert=True).all()

    # Only admins
    admins = User.query.filter_by(is_admin=True).all()

    # Count users
    total = User.query.count()
    print(f"Total registered users: {total}")

    # Find user by username
    user = User.query.filter_by(username='admin').first()

    # All forum posts (newest first)
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()

    # Available expert profiles
    experts_profiles = ExpertProfile.query.filter_by(is_available=True).all()""")

    pdf.sub('Method B: SQLite Command-Line Interface (CLI)')
    pdf.code("""\
# Open SQLite in project folder
sqlite3 instance/community.db

.tables                            -- List all tables
.schema users                      -- Show table structure

-- All registered users
SELECT id, username, email, is_admin, is_expert, created_at FROM users;

-- Count total users
SELECT COUNT(*) AS total_users FROM users;

-- Experts only
SELECT id, username, email FROM users WHERE is_expert = 1;

-- Admins only
SELECT id, username, email FROM users WHERE is_admin = 1;

-- Forum posts with author names
SELECT fp.id, fp.title, u.username, fp.created_at
FROM forum_posts fp JOIN users u ON u.id = fp.author_id
ORDER BY fp.created_at DESC;

-- Expert profiles with user info
SELECT u.username, u.email, ep.specializations, ep.hourly_rate, ep.average_rating
FROM expert_profiles ep JOIN users u ON u.id = ep.user_id;

-- Consultation bookings
SELECT cb.id, u.username AS farmer, cb.booking_date, cb.mode, cb.status
FROM consultation_bookings cb JOIN users u ON u.id = cb.farmer_id;

.quit""")

    pdf.sub('Method C: DB Browser for SQLite (GUI Tool)')
    pdf.para(
        '1. Download from: https://sqlitebrowser.org/\n'
        '2. Open file:  instance/community.db\n'
        '3. Use "Browse Data" tab to see all rows in any table visually.\n'
        '4. Use "Execute SQL" tab to run any of the queries above.'
    )


def view_users(pdf):
    pdf.add_page()
    pdf.hdr('6. HOW TO VIEW REGISTERED USERS')

    pdf.sub('Option 1 - Admin Web Panel (In-App)')
    pdf.para(
        'Log in as admin (username: admin, password: admin123).\n'
        'Navigate to the Admin Dashboard via the top navigation menu. '
        'The admin panel lists all registered users with roles, dates, and activity.'
    )

    pdf.sub('Option 2 - Quick Python One-Liner')
    pdf.code("""\
python -c "
from flask import Flask; from community_models import db, User
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/community.db'
app.config['SECRET_KEY'] = 'x'
db.init_app(app)
with app.app_context():
    users = User.query.order_by(User.created_at).all()
    print(f'Total users: {len(users)}')
    for u in users:
        print(u.id, u.username, u.email, 'ADMIN' if u.is_admin else '',
              'EXPERT' if u.is_expert else '', str(u.created_at)[:10])
" """)

    pdf.sub('Option 3 - SQLite CLI One-Liner')
    pdf.code(
        'sqlite3 instance/community.db '
        '"SELECT id,username,email,is_admin,is_expert,created_at FROM users ORDER BY created_at;"'
    )

    pdf.sub('Default Seeded Test Accounts')
    pdf.tbl_hdr([('Username', 42), ('Password', 34), ('Role', 32), ('Email', 0)])
    rows = [
        ('admin',       'admin123',  'Administrator', 'admin@cropdoctor.com'),
        ('john_farmer', 'farmer123', 'Farmer',        'john@example.com'),
        ('dr_sarah',    'expert123', 'Expert (PhD)',   'sarah@example.com'),
    ]
    for i, r in enumerate(rows):
        pdf.tbl_row(list(zip(r, [42, 34, 32, 0])), fill=(i % 2 == 0))

    pdf.ln(4)
    pdf.set_fill_color(255, 240, 200)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 8, S('  WARNING: Change all default passwords before production deployment!'),
             border=0, new_x='LMARGIN', new_y='NEXT', fill=True)


def api_endpoints(pdf):
    pdf.add_page()
    pdf.hdr('7. API ENDPOINTS REFERENCE')

    endpoints = [
        ('GET',  '/',                               'Landing / login page'),
        ('GET',  '/login',                          'Show login form'),
        ('POST', '/login',                          'Authenticate user & start session'),
        ('GET',  '/register',                       'Show registration form'),
        ('POST', '/register',                       'Create new user account'),
        ('GET',  '/logout',                         'End user session'),
        ('GET',  '/home',                           'Main dashboard (requires login)'),
        ('POST', '/predict',                        'Crop recommendation (JSON: N,P,K,temp,humidity,ph,rainfall)'),
        ('POST', '/analyze',                        'Disease detection (multipart: image file upload)'),
        ('GET',  '/download-report/<filename>',     'Download generated PDF report'),
        ('GET',  '/weather',                        'Get current weather for user location'),
        ('GET',  '/history',                        'View past analysis history'),
        ('GET',  '/community',                      'Community forum home'),
        ('GET',  '/forum/post/<id>',                'View forum post with comments'),
        ('POST', '/api/forum/posts',                'Create a new forum post (JSON body)'),
        ('POST', '/api/forum/posts/<id>/comments',  'Add comment to post'),
        ('POST', '/api/forum/posts/<id>/vote',      'Upvote or downvote a post'),
        ('GET',  '/api/experts',                    'List available agricultural experts'),
        ('POST', '/api/experts/book',               'Book an expert consultation'),
        ('GET',  '/api/bookings',                   "View farmer's consultation bookings"),
        ('GET',  '/profile/<username>',             'View user public profile'),
    ]

    pdf.tbl_hdr([('Method', 20), ('Endpoint', 74), ('Description', 0)])
    GET_C  = (232, 245, 232)
    POST_C = (232, 240, 255)
    for i, (method, path, desc) in enumerate(endpoints):
        c = GET_C if method == 'GET' else POST_C
        pdf.set_fill_color(*c)
        pdf.tbl_row([(method, 20), (path, 74), (desc, 0)], fill=True)


def ml_models(pdf):
    pdf.add_page()
    pdf.hdr('8. MACHINE LEARNING MODELS')

    pdf.sub('A. Crop Recommendation Model')
    for k, v in [
        ('Algorithm',     'Random Forest Classifier (scikit-learn)'),
        ('Training Data', 'Crop_recommendation.csv - 2,200 rows, 22 crop classes'),
        ('Input Features','N (Nitrogen), P (Phosphorus), K (Potassium), Temperature (C), Humidity (%), pH, Rainfall (mm)'),
        ('Output',        'Predicted crop label + probability for all 22 crops (top-3 shown with confidence bars)'),
        ('Saved Files',   'models/crop_recommendation_model.pkl, models/label_encoder.pkl'),
        ('Scalers',       'minmaxscaler.pkl and standscaler.pkl for feature normalisation'),
    ]:
        pdf.kv(k, v)

    pdf.ln(3)
    pdf.sub('B. Plant Disease Detection Model')
    for k, v in [
        ('Architecture',  'Convolutional Neural Network (CNN) via TensorFlow/Keras'),
        ('Dataset',       'PlantVillage dataset - 38 classes (14 plant types, diseased + healthy)'),
        ('Input',         'RGB image resized to 224x224 pixels, normalised to [0,1]'),
        ('Model Files',   'models/plant_disease_model.h5  OR  models/plant_disease_model/ (SavedModel)'),
        ('Fallback',      'analyze_image_enhanced() - colour-heuristic using RGB ratios and pixel masks'),
        ('Output',        'Disease class, confidence %, severity, treatment, prevention; downloadable PDF'),
    ]:
        pdf.kv(k, v)

    pdf.ln(3)
    pdf.sub('C. Supported Crops & Diseases')
    diseases = [
        'Apple: Apple Scab, Black Rot, Cedar Apple Rust',
        'Corn/Maize: Cercospora Leaf Spot, Common Rust, Northern Leaf Blight',
        'Grape: Black Rot, Esca (Black Measles), Leaf Blight',
        'Peach: Bacterial Spot',
        'Pepper: Bacterial Spot',
        'Potato: Early Blight, Late Blight',
        'Strawberry: Leaf Scorch',
        'Tomato: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus',
        'Blueberry, Cherry, Raspberry, Soybean, Squash, Orange: Healthy class only',
    ]
    for d in diseases:
        pdf.bul(d)

    pdf.ln(2)
    pdf.sub('D. 22 Crop Classes (Recommendation)')
    crops = 'Rice, Maize, Chickpea, Kidney Beans, Pigeon Peas, Moth Beans, Mung Bean, Black Gram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee'
    pdf.para(crops)


def community(pdf):
    pdf.add_page()
    pdf.hdr('9. COMMUNITY & EXPERT CONSULTATION FEATURES')

    pdf.sub('Forum Categories')
    for f in ['Crop Management', 'Pest Control', 'Irrigation & Water Management',
               'Soil Health', 'Market Trends', 'Success Stories', 'Q&A', 'Equipment & Technology']:
        pdf.bul(f)

    pdf.ln(2)
    pdf.para(
        'Forum features: nested comments/replies, upvote/downvote on posts and comments, '
        'post flagging for moderation, "solved" status, pinned/locked posts, tag filtering, '
        'optional image attachments, and view counters.'
    )

    pdf.sub('Expert Consultation System')
    for item in [
        'Browse verified agronomists with specializations, credentials, hourly rate (KSh), experience',
        'Booking modes: Video, Phone, Chat, In-Person',
        'Availability scheduling: day-of-week + time-slot based',
        'Booking states: Pending -> Confirmed -> Completed / Cancelled',
        'Post-consultation reviews (1-5 stars with text feedback)',
        'Expert badges: Top Rated, Verified Specialist, etc.',
    ]:
        pdf.bul(item)

    pdf.sub('Reputation & Gamification')
    for item in [
        'Users earn reputation points for posting, answering, receiving upvotes',
        'Badges awarded for milestones: Contributor, Helper, Expert Mentor',
        'Reputation log tracks every point change with action type and reference ID',
    ]:
        pdf.bul(item)

    pdf.sub('User Roles')
    roles = [
        ('Regular Farmer',         'Post in forum, book experts, view analyses, earn reputation'),
        ('Expert (is_expert=True)','Has ExpertProfile, receive bookings, set availability, add consultation notes'),
        ('Admin (is_admin=True)',  'Full access: manage users, moderate forum, view all data'),
    ]
    for role, perms in roles:
        pdf.kv(role, perms, kw=55)


def probable_questions(pdf):
    sections = [
        ('A. System Overview Questions', [
            ('What is CropDoctor and what problem does it solve?',
             'A web-based agricultural AI platform that helps farmers choose the right crop to plant and identify plant diseases, addressing food security gaps.'),
            ('Who are the target users of this system?',
             'Smallholder farmers, commercial farmers, extension officers, agronomists, and agricultural experts.'),
            ('What are the three main functional modules?',
             '1) Crop Recommendation Engine, 2) Plant Disease Detection, 3) Community Hub (forum + expert consultations).'),
            ('How does this system help farmers without agricultural expertise?',
             'Provides AI-driven crop suggestions, disease diagnosis with treatment advice, fertilizer schedules, and downloadable PDF reports - all via a browser.'),
            ('What differentiates CropDoctor from a simple internet search?',
             'ML models trained on real data, personalised recommendations based on exact soil parameters, expert consultation booking, and community peer support.'),
            ('What crops can the system recommend?',
             '22 classes: Rice, Maize, Chickpea, Kidney Beans, Lentil, Banana, Mango, Apple, Orange, Cotton, Coffee, Jute, and more.'),
            ('What is the significance of fertilizer recommendations?',
             'Provides specific NPK ratios, application rates, timing schedules, organic alternatives, and micronutrient advice per crop type.'),
        ]),
        ('B. Technical / Architecture Questions', [
            ('What web framework is used and why Flask?',
             'Flask 3.0.3 - lightweight, Pythonic, easy ML integration, no overhead, large ecosystem.'),
            ('Explain the MVC pattern in this project.',
             'Models: SQLAlchemy ORM classes; Views: Jinja2 HTML templates; Controllers: Flask route functions in app.py.'),
            ('How are passwords stored securely?',
             'Werkzeug generate_password_hash (PBKDF2-SHA256) - never plain-text; check_password_hash for verification.'),
            ('What is Flask-Login and its role?',
             'Manages user sessions, current_user proxy, @login_required decorator, and login_view redirect.'),
            ('How does the system handle file uploads?',
             'Werkzeug secure_filename, allowed extensions {png,jpg,jpeg}, 16 MB limit, stored in uploads/ folder.'),
            ('What is the .env file for?',
             'Stores SECRET_KEY, SQLALCHEMY_DATABASE_URI, and API keys outside the codebase using python-dotenv.'),
            ('Explain image preprocessing for disease detection.',
             'Pillow opens image -> convert RGB -> resize 224x224 -> divide by 255.0 -> np.expand_dims for batch (1,224,224,3).'),
            ('What fallback exists if TensorFlow unavailable?',
             'analyze_image_enhanced() - a colour-heuristic classifier using R/G/B channel statistics and pixel masks.'),
            ('What is the maximum upload file size?',
             '16 MB, set via app.config[MAX_CONTENT_LENGTH] = 16 * 1024 * 1024.'),
            ('How does the JSON API work for crop recommendation?',
             'POST /predict with JSON body {N, P, K, temperature, humidity, ph, rainfall} returns top-N crop predictions.'),
        ]),
        ('C. Database / SQL Questions', [
            ('What database does the system use? Why SQLite?',
             'SQLite - zero-configuration, serverless, file-based. Ideal for development and small deployments.'),
            ('How many tables are in the database? Name them.',
             '15+ tables: users, user_profiles, forum_categories, forum_posts, forum_comments, post_votes, comment_votes, post_flags, expert_profiles, expert_availability, consultation_bookings, consultation_reviews, expert/user_badges, reputation_logs, notifications.'),
            ('Write SQL to list all registered users.',
             'SELECT id, username, email, is_admin, is_expert, created_at FROM users ORDER BY created_at;'),
            ('Write SQL to find all expert users.',
             'SELECT username, email FROM users WHERE is_expert = 1;'),
            ('Write SQL to count registered users.',
             'SELECT COUNT(*) AS total FROM users;'),
            ('How is data integrity enforced?',
             'SQLAlchemy ForeignKeys, UniqueConstraints (e.g., unique_post_vote on post_id+user_id), cascade delete on child records.'),
            ('What is UserMixin from Flask-Login?',
             'Provides default is_authenticated, is_active, is_anonymous, get_id() implementations required by Flask-Login.'),
            ('How are self-referential comments handled?',
             'ForumComment has parent_comment_id FK referencing itself (same table) for nested reply threads.'),
            ('How do you reset the database?',
             'Delete instance/community.db then run: python database_setup.py to recreate and reseed tables.'),
            ('What is the SQLALCHEMY_DATABASE_URI for this project?',
             'sqlite:///instance/community.db (relative path to the instance/ folder)'),
        ]),
        ('D. Machine Learning Questions', [
            ('What ML algorithm is used for crop recommendation?',
             'Random Forest Classifier from scikit-learn, trained on 7 numeric soil/climate features.'),
            ('What are the 7 input features for crop recommendation?',
             'Nitrogen (N), Phosphorus (P), Potassium (K), Temperature (C), Humidity (%), pH, Rainfall (mm).'),
            ('What training dataset is used?',
             'Crop_recommendation.csv - 2,200 rows across 22 crop classes.'),
            ('Why Random Forest over other algorithms?',
             'Handles non-linear feature interactions, robust to outliers, provides feature importance, high accuracy on tabular data.'),
            ('How many disease classes does the CNN support?',
             '38 classes covering 14 plant types (diseased and healthy variants) from PlantVillage dataset.'),
            ('What is the CNN input image size?',
             '224x224 RGB image - same as VGG16/ResNet standard input for transfer learning compatibility.'),
            ('How are model files loaded at startup?',
             'pickle.load() for crop model and label encoder; keras.models.load_model() for CNN at app initialisation.'),
            ('What does the confidence percentage represent?',
             'Softmax output probability (0-100%) from model.predict(); or a rule-based score in the heuristic fallback.'),
            ('What are model scalers used for?',
             'minmaxscaler.pkl and standscaler.pkl normalise input features to the same scale as training data before prediction.'),
        ]),
        ('E. Security Questions', [
            ('How is unauthorised access prevented?',
             'Flask-Login @login_required decorator redirects unauthenticated requests to the login page.'),
            ('How is XSS prevented in forum posts?',
             'bleach 6.1.0 sanitises all user HTML before storing/rendering in forum posts.'),
            ('What is CSRF protection?',
             'Flask-WTF embeds hidden CSRF tokens in all forms; POST requests validate the token before processing.'),
            ('What if a non-image file is uploaded?',
             'allowed_extensions() rejects files not in {png, jpg, jpeg} with an error before any processing.'),
            ('What must change before production deployment?',
             'SECRET_KEY, admin password (admin123 is seeded), enable HTTPS, set DEBUG=False, use stronger DB passwords.'),
            ('How is the admin account different from regular users?',
             'is_admin=True flag. Admin has access to moderation, user management, and all data via admin routes.'),
        ]),
        ('F. Community / Forum Questions', [
            ('List all forum categories.',
             'Crop Management, Pest Control, Irrigation & Water Management, Soil Health, Market Trends, Success Stories, Q&A, Equipment & Technology.'),
            ('Explain the reputation/gamification system.',
             'Users earn points for posts, upvotes received, best answers marked. Points unlock badges: Contributor, Helper, Expert Mentor.'),
            ('How does expert consultation booking work?',
             'Farmer browses experts -> selects -> chooses date/time/mode -> pending booking -> expert confirms -> consultation -> farmer reviews.'),
            ('What consultation modes are available?',
             'Video, Phone, Chat, and In-Person sessions.'),
            ('How are expert availability slots defined?',
             'ExpertAvailability model: day_of_week (0=Monday), start_time, end_time. Experts configure slots for Monday-Friday.'),
            ('What is a ConsultationReview?',
             'A 1-5 star rating with text feedback submitted by a farmer after a completed consultation, linked to the booking.'),
        ]),
        ('G. Practical / How-To Questions', [
            ('How do you start the CropDoctor server?',
             'Run: python app.py in the project root. Access at http://127.0.0.1:5000'),
            ('How do you view registered users without the UI?',
             'sqlite3 instance/community.db then: SELECT username, email, is_admin FROM users;'),
            ('How do you add a new crop to fertiliser recommendations?',
             'Add a new key-value entry to the FERTILIZER_INFO dictionary in app.py.'),
            ('How do you generate a disease PDF report?',
             'Upload image on Disease Detection page -> analysis runs -> click "Download Report" -> pdf_generator.generate_report() creates PDF in uploads/'),
            ('How do you train the crop recommendation model?',
             'Run: python train_crop_model.py  Saves model to models/crop_recommendation_model.pkl'),
            ('How do you install all dependencies?',
             'pip install -r requirements.txt'),
            ('What port does the application run on?',
             'Flask default port 5000. Access: http://localhost:5000'),
            ('How do you download the PlantVillage model/dataset?',
             'Run download_kaggle.py or use try_hub_load.py which uses the kagglehub library.'),
        ]),
    ]

    for si, (section_title, qs) in enumerate(sections):
        pdf.add_page()
        pdf.hdr('10. PROBABLE INTERVIEW / VIVA / EXAM QUESTIONS', r=0, g=60, b=120)
        pdf.sub(section_title)
        pdf.line_sep()
        for qi, (q, a) in enumerate(qs, 1):
            pdf.qa(qi, q, a)
            pdf.line_sep()


def quick_ref(pdf):
    pdf.add_page()
    pdf.hdr('11. QUICK REFERENCE CARD', r=100, g=0, b=0)

    pdf.sub('Start the Application')
    pdf.code('cd "e:/crop and disease reccommendation/Crop-Recommendation-and-Disease-Detection-System"\npython app.py\n# Access at: http://localhost:5000')

    pdf.sub('Default Login Credentials')
    pdf.code("""\
Admin:   username=admin       password=admin123
Farmer:  username=john_farmer  password=farmer123
Expert:  username=dr_sarah     password=expert123""")

    pdf.sub('View All Registered Users')
    pdf.code('sqlite3 instance/community.db "SELECT id,username,email,is_admin,is_expert FROM users;"')

    pdf.sub('Reset & Re-seed Database')
    pdf.code('del instance\\community.db\npython database_setup.py')

    pdf.sub('Install Dependencies')
    pdf.code('pip install -r requirements.txt')

    pdf.sub('Train Crop Model')
    pdf.code('python train_crop_model.py')

    pdf.sub('Key Files')
    pdf.code("""\
app.py              <- Main Flask app (crop recommendation + disease detection)
app_community.py    <- Community routes (login, register, profile)
community_models.py <- All SQLAlchemy DB models (15+ tables)
database_setup.py   <- DB init + seeding default users
pdf_generator.py    <- Disease analysis PDF reports
expert_api.py       <- Expert consultation REST API
forum_api.py        <- Forum posts/comments REST API
models/             <- ML model files (.pkl, .h5)
instance/community.db  <- SQLite database
uploads/            <- User images + generated PDF reports
.env                <- Environment variables (SECRET_KEY, DB URI)""")

    pdf.ln(4)
    pdf.sub('Common SQL Queries at a Glance')
    pdf.code("""\
SELECT COUNT(*) FROM users;                         -- Total users
SELECT * FROM users WHERE is_admin=1;               -- Admins
SELECT * FROM users WHERE is_expert=1;              -- Experts
SELECT * FROM forum_posts ORDER BY created_at DESC; -- Latest posts
SELECT * FROM expert_profiles WHERE is_available=1; -- Available experts
SELECT * FROM consultation_bookings WHERE status='pending'; -- Pending bookings""")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def build_pdf():
    pdf = Doc()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.alias_nb_pages()

    cover(pdf)
    system_overview(pdf)
    tech_stack(pdf)
    architecture(pdf)
    db_schema(pdf)
    db_queries(pdf)
    view_users(pdf)
    api_endpoints(pdf)
    ml_models(pdf)
    community(pdf)
    probable_questions(pdf)
    quick_ref(pdf)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'CropDoctor_System_Documentation.pdf')
    pdf.output(out)
    print(f'\n[SUCCESS] PDF saved: {out}')
    return out


if __name__ == '__main__':
    build_pdf()
