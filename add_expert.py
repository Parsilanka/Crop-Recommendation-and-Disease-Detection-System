"""
Helper script to add a new expert to the CropDoctor database.
Run this script from the terminal to create new experts.
"""
import os
from datetime import time
from flask import Flask
from community_models import db, User, ExpertProfile, ExpertAvailability

def add_new_expert(username, email, password, full_name, credentials, specializations, rate):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        # 1. Check if user already exists
        if User.query.filter_by(username=username).first():
            print(f"[-] A user with username '{username}' already exists.")
            return

        print(f"[*] Adding new expert: {full_name} ({username})...")
        
        # 2. Create the User account
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            location='Kenya',
            is_expert=True,
            is_verified=True,
            reputation_points=100
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit() # Commit to get the new_user.id
        
        # 3. Create the ExpertProfile
        expert_profile = ExpertProfile(
            user_id=new_user.id,
            specializations=specializations,
            credentials=credentials,
            bio=f'Expert agronomist specializing in {specializations}.',
            hourly_rate=float(rate),
            years_experience=5,
            languages='English, Swahili',
            consultation_modes='video,phone,chat',
            is_verified=True,
            is_available=True,
            average_rating=0.0
        )
        db.session.add(expert_profile)
        db.session.commit() # Commit to get expert_profile.id
        
        # 4. Add standard availability (Mon-Fri, 9AM-5PM)
        for day in range(5):
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
        print(f"[+] Successfully added {full_name} to the database as an expert!")

if __name__ == '__main__':
    print("--- Add a New Expert ---")
    u_name = input("Enter username (e.g., dr_smith): ")
    u_email = input("Enter email: ")
    u_pass = input("Enter password: ")
    u_full = input("Enter full name (e.g., Dr. John Smith): ")
    u_cred = input("Enter credentials (e.g., PhD Agronomy): ")
    u_spec = input("Enter specializations (e.g., Soil Science, Pathology): ")
    u_rate = input("Enter hourly rate in KSh (e.g., 1000): ")
    
    add_new_expert(u_name, u_email, u_pass, u_full, u_cred, u_spec, u_rate)
