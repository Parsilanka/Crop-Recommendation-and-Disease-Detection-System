"""
Integrated Community Features App
Combines existing crop/disease detection with forum and expert consultation
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import existing modules
import history
import pdf_generator
import weather

# Import community modules
from community_models import db, User
from forum_api import forum_bp
from expert_api import expert_bp

# Import existing disease detection logic
from app import (MODEL_AVAILABLE, model, model_loaded, load_trained_model,
                 DISEASE_CLASSES, DISEASE_INFO, get_disease_info,
                 preprocess_image_for_ml, analyze_image_enhanced,
                 crop_model, crop_le, get_fertilizer_recommendation,
                 ALLOWED_EXTENSIONS)

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///community.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Pagination settings
app.config['POSTS_PER_PAGE'] = int(os.getenv('POSTS_PER_PAGE', 20))
app.config['EXPERTS_PER_PAGE'] = int(os.getenv('EXPERTS_PER_PAGE', 12))

# Reputation points
app.config['POINTS_POST_CREATED'] = int(os.getenv('POINTS_POST_CREATED', 5))
app.config['POINTS_COMMENT_CREATED'] = int(os.getenv('POINTS_COMMENT_CREATED', 2))
app.config['POINTS_UPVOTE_RECEIVED'] = int(os.getenv('POINTS_UPVOTE_RECEIVED', 10))
app.config['POINTS_BEST_ANSWER'] = int(os.getenv('POINTS_BEST_ANSWER', 50))
app.config['POINTS_EXPERT_REVIEW'] = int(os.getenv('POINTS_EXPERT_REVIEW', 15))

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(forum_bp)
app.register_blueprint(expert_bp)

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        location = data.get('location')
        phone = data.get('phone')
        
        # Validate
        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            location=location,
            phone=phone
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Registration successful', 'user_id': user.id}), 201
    
    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = db.func.now()
            db.session.commit()
            
            # Handle post-login redirection
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            
            return jsonify({'message': 'Login successful', 'redirect': next_page}), 200
        
        return jsonify({'error': 'Invalid username or password'}), 401
    
    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html', user=current_user)


# ============================================================================
# MAIN ROUTES (Existing functionality)
# ============================================================================

@app.route('/')
@login_required
def index():
    """Main dashboard"""
    return render_template('index.html')
    """Main dashboard"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
@app.route('/recommend_crop', methods=['POST'])
def recommend_crop():
    """Crop recommendation endpoint (existing)"""
    try:
        data = request.get_json()
        
        # Extract features
        N = float(data.get('nitrogen', 0))
        P = float(data.get('phosphorus', 0))
        K = float(data.get('potassium', 0))
        temperature = float(data.get('temperature', 25))
        humidity = float(data.get('humidity', 65))
        ph = float(data.get('ph') or data.get('pH') or 6.5)
        rainfall = float(data.get('rainfall', 100))
        
        # Use ML model if available
        if crop_model and crop_le:
            import numpy as np
            features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            
            # Get prediction probabilities
            probabilities = crop_model.predict_proba(features)[0]
            
            # Get top 3 recommendations
            top_indices = probabilities.argsort()[-3:][::-1]
            recommendations = []
            
            for idx in top_indices:
                crop_name = crop_le.classes_[idx]
                confidence = probabilities[idx] * 100
                
                recommendations.append({
                    'crop': crop_name,
                    'confidence': round(confidence, 2),
                    'fertilizer': get_fertilizer_recommendation(crop_name)
                })
            
            return jsonify({
                'success': True,
                'recommendations': recommendations
            })
        else:
            return jsonify({'error': 'Crop recommendation model not available'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/classify_disease', methods=['POST'])
def classify_disease():
    """Disease classification endpoint (existing)"""
    try:
        if 'file' not in request.files and 'image' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files.get('file') or request.files.get('image')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Use ML model if available, otherwise use color-based detection
            if model_loaded and model:
                img_array = preprocess_image_for_ml(filepath)
                predictions = model.predict(img_array)
                predicted_class_idx = predictions[0].argmax()
                confidence = float(predictions[0][predicted_class_idx]) * 100
                disease_name = DISEASE_CLASSES[predicted_class_idx]
            else:
                disease_name, confidence = analyze_image_enhanced(filepath)
            
            disease_info = get_disease_info(disease_name)
            
            result = {
                'disease': disease_name,
                'confidence': round(confidence, 2),
                'severity': disease_info['severity'],
                'treatment': disease_info['treatment'],
                'prevention': disease_info['prevention']
            }
            
            # Save to history
            history.add_entry(filename, disease_name, confidence)
            
            return jsonify(result)
        
        return jsonify({'error': 'Invalid file type'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/history')
def get_history():
    """View analysis history"""
    import history
    entries = history.get_history()
    return render_template('history.html', entries=entries)


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/download_report/<int:report_id>')
def download_report(report_id):
    """Generate and download PDF report"""
    try:
        import sqlite3
        from app import get_disease_info
        
        # Get entry from history
        conn = sqlite3.connect(history.DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM history WHERE id = ?', (report_id,))
        entry = c.fetchone()
        conn.close()
        
        if not entry:
            return "Report not found", 404
            
        # Get details
        disease_info = get_disease_info(entry['prediction'])
        
        # Generate PDF
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], entry['filename'])
        image_path = os.path.abspath(image_path)
        
        # We need to ensure pdf_generator is imported and working
        report_file, report_path = pdf_generator.generate_report(
            image_path, 
            entry['prediction'], 
            entry['confidence'], 
            disease_info
        )
        
        from flask import send_file
        return send_file(report_path, as_attachment=True)
        
    except Exception as e:
        print(f"Error in download_report: {e}")
        return str(e), 400


@app.route('/weather_data')
def weather_data():
    """Get weather data"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    data = weather.get_weather(lat, lon)
    if data:
        data['desc'] = weather.get_weather_desc(data['weathercode'])
        return jsonify(data)
    return jsonify({'error': 'Could not fetch weather'}), 500


# ============================================================================
# COMMUNITY ROUTES
# ============================================================================

@app.route('/forum')
def forum():
    """Forum homepage"""
    return render_template('forum.html')


@app.route('/forum/post/<int:post_id>')
def forum_post(post_id):
    """Individual forum post view"""
    return render_template('forum_post.html', post_id=post_id)


@app.route('/forum/create')
@login_required
def forum_create():
    """Create new forum post"""
    return render_template('forum_create.html')


@app.route('/experts')
def experts():
    """Expert directory"""
    return render_template('experts.html')


@app.route('/experts/<int:expert_id>')
def expert_profile(expert_id):
    """Expert profile page"""
    return render_template('expert_profile.html', expert_id=expert_id)


@app.route('/booking/<int:expert_id>')
@login_required
def booking(expert_id):
    """Booking page"""
    return render_template('booking.html', expert_id=expert_id)


@app.route('/my-bookings')
@login_required
def my_bookings():
    """User's bookings"""
    return render_template('my_bookings.html')


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("CROP DOCTOR - COMMUNITY EDITION")
    print("="*60)
    print("\nFeatures:")
    print("  [+] Crop Recommendation")
    print("  [+] Disease Detection")
    print("  [+] Community Forum")
    print("  [+] Expert Consultation")
    print("\n" + "="*60)
    
    # Load ML model for disease detection
    if MODEL_AVAILABLE:
        print("\n[INFO] TensorFlow available")
        load_trained_model()
    else:
        print("\n[WARNING] TensorFlow not available")
        print("  Using enhanced color-based disease detection")
    
    print("\n" + "="*60)
    print("Starting Flask server...")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
