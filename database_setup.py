"""
Database Setup and Initialization Script
Creates all tables and seeds initial data
"""

from community_models import db, ForumCategory, User, ExpertProfile, ExpertAvailability
from datetime import time
import os

def init_database(app):
    """Initialize database with tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("[OK] Database tables created successfully!")
        
        # Seed initial data
        seed_forum_categories()
        seed_sample_users()
        print("[OK] Database initialized successfully!")


def seed_forum_categories():
    """Create initial forum categories"""
    categories = [
        {
            'name': 'Crop Management',
            'description': 'Discussions about crop cultivation, planting, and harvesting',
            'icon': '🌾',
            'slug': 'crop-management'
        },
        {
            'name': 'Pest Control',
            'description': 'Identify and manage pests and diseases',
            'icon': '🐛',
            'slug': 'pest-control'
        },
        {
            'name': 'Irrigation & Water Management',
            'description': 'Water conservation and irrigation techniques',
            'icon': '💧',
            'slug': 'irrigation'
        },
        {
            'name': 'Soil Health',
            'description': 'Soil testing, fertilization, and improvement',
            'icon': '🌱',
            'slug': 'soil-health'
        },
        {
            'name': 'Market Trends',
            'description': 'Crop prices, market opportunities, and selling strategies',
            'icon': '📈',
            'slug': 'market-trends'
        },
        {
            'name': 'Success Stories',
            'description': 'Share your farming success stories and experiences',
            'icon': '🏆',
            'slug': 'success-stories'
        },
        {
            'name': 'Q&A',
            'description': 'Quick questions and answers',
            'icon': '❓',
            'slug': 'qa'
        },
        {
            'name': 'Equipment & Technology',
            'description': 'Farm equipment, tools, and agricultural technology',
            'icon': '🚜',
            'slug': 'equipment'
        }
    ]
    
    for cat_data in categories:
        # Check if category already exists
        existing = ForumCategory.query.filter_by(slug=cat_data['slug']).first()
        if not existing:
            category = ForumCategory(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    print(f"[OK] Created {len(categories)} forum categories")


def seed_sample_users():
    """Create sample users for testing"""
    
    # Check if admin already exists
    if User.query.filter_by(username='admin').first():
        print("[OK] Sample users already exist")
        return
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@cropdoctor.com',
        full_name='System Administrator',
        location='Nairobi',
        is_admin=True,
        is_verified=True,
        reputation_points=1000
    )
    admin.set_password('admin123')  # Change in production!
    db.session.add(admin)
    
    # Create sample farmer
    farmer = User(
        username='john_farmer',
        email='john@example.com',
        full_name='John Kamau',
        location='Kiambu',
        phone='+254712345678',
        is_verified=True,
        reputation_points=150
    )
    farmer.set_password('farmer123')
    db.session.add(farmer)
    
    # Create sample expert
    expert_user = User(
        username='dr_sarah',
        email='sarah@example.com',
        full_name='Dr. Sarah Mwangi',
        location='Nairobi',
        phone='+254723456789',
        is_expert=True,
        is_verified=True,
        reputation_points=500
    )
    expert_user.set_password('expert123')
    db.session.add(expert_user)
    
    db.session.commit()
    
    # Create expert profile for dr_sarah
    expert_profile = ExpertProfile(
        user_id=expert_user.id,
        specializations='Plant Pathology, Disease Diagnosis, Soil Health',
        credentials='PhD in Plant Pathology, MSc Agriculture, Certified Crop Consultant',
        bio='Experienced plant pathologist with 8 years of experience helping farmers diagnose and treat crop diseases. Specializing in tomato, potato, and maize diseases.',
        hourly_rate=1500.0,  # KSh
        years_experience=8,
        languages='English, Swahili, Kikuyu',
        consultation_modes='video,phone,chat,in-person',
        is_verified=True,
        is_available=True,
        average_rating=4.8
    )
    db.session.add(expert_profile)
    db.session.commit()
    
    # Add availability for expert (Monday to Friday, 9 AM - 5 PM)
    for day in range(5):  # Monday to Friday
        morning_slot = ExpertAvailability(
            expert_id=expert_profile.id,
            day_of_week=day,
            start_time=time(9, 0),
            end_time=time(13, 0)
        )
        afternoon_slot = ExpertAvailability(
            expert_id=expert_profile.id,
            day_of_week=day,
            start_time=time(14, 0),
            end_time=time(17, 0)
        )
        db.session.add(morning_slot)
        db.session.add(afternoon_slot)
    
    db.session.commit()
    print("[OK] Created sample users (admin, farmer, expert)")
    print("\n" + "="*60)
    print("SAMPLE LOGIN CREDENTIALS (Change in production!):")
    print("="*60)
    print("Admin:  username='admin'      password='admin123'")
    print("Farmer: username='john_farmer' password='farmer123'")
    print("Expert: username='dr_sarah'    password='expert123'")
    print("="*60 + "\n")


if __name__ == '__main__':
    from flask import Flask
    from community_models import db
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    db.init_app(app)
    
    print("\n" + "="*60)
    print("INITIALIZING COMMUNITY DATABASE")
    print("="*60 + "\n")
    
    init_database(app)
    
    print("\n" + "="*60)
    print("DATABASE SETUP COMPLETE!")
    print("="*60 + "\n")
