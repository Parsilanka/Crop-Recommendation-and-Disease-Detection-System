"""
Expert Consultation API Endpoints
Handles expert profiles, bookings, and reviews
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from community_models import (db, ExpertProfile, ExpertAvailability, ConsultationBooking, 
                               ConsultationReview, User, ExpertBadge)
from datetime import datetime, date, time, timedelta
from sqlalchemy import and_, or_

expert_bp = Blueprint('expert', __name__, url_prefix='/api/experts')


@expert_bp.route('', methods=['GET'])
def get_experts():
    """Get all experts with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('EXPERTS_PER_PAGE', 12)
    specialization = request.args.get('specialization')
    location = request.args.get('location')
    min_rating = request.args.get('min_rating', type=float)
    max_rate = request.args.get('max_rate', type=float)
    sort_by = request.args.get('sort', 'rating')  # rating, experience, price
    
    query = ExpertProfile.query.filter_by(is_available=True, is_verified=True)
    
    # Apply filters
    if specialization:
        query = query.filter(ExpertProfile.specializations.contains(specialization))
    if location:
        query = query.join(User).filter(User.location == location)
    if min_rating:
        query = query.filter(ExpertProfile.average_rating >= min_rating)
    if max_rate:
        query = query.filter(ExpertProfile.hourly_rate <= max_rate)
    
    # Apply sorting
    if sort_by == 'rating':
        query = query.order_by(ExpertProfile.average_rating.desc())
    elif sort_by == 'experience':
        query = query.order_by(ExpertProfile.years_experience.desc())
    elif sort_by == 'price':
        query = query.order_by(ExpertProfile.hourly_rate.asc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    experts = []
    for expert in pagination.items:
        experts.append({
            'id': expert.id,
            'user': {
                'id': expert.user.id,
                'username': expert.user.username,
                'full_name': expert.user.full_name,
                'location': expert.user.location
            },
            'specializations': expert.specializations.split(',') if expert.specializations else [],
            'bio': expert.bio,
            'hourly_rate': expert.hourly_rate,
            'years_experience': expert.years_experience,
            'languages': expert.languages.split(',') if expert.languages else [],
            'consultation_modes': expert.consultation_modes.split(',') if expert.consultation_modes else [],
            'total_consultations': expert.total_consultations,
            'average_rating': expert.average_rating,
            'is_verified': expert.is_verified
        })
    
    return jsonify({
        'experts': experts,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })


@expert_bp.route('/<int:expert_id>', methods=['GET'])
def get_expert(expert_id):
    """Get expert profile with reviews"""
    expert = ExpertProfile.query.get_or_404(expert_id)
    
    # Get recent reviews
    reviews = []
    recent_bookings = ConsultationBooking.query.filter_by(
        expert_id=expert_id,
        status='completed'
    ).order_by(ConsultationBooking.updated_at.desc()).limit(10).all()
    
    for booking in recent_bookings:
        if booking.review:
            reviews.append({
                'id': booking.review.id,
                'rating': booking.review.rating,
                'review_text': booking.review.review_text,
                'would_recommend': booking.review.would_recommend,
                'farmer': {
                    'username': booking.farmer.username
                },
                'created_at': booking.review.created_at.isoformat()
            })
    
    return jsonify({
        'id': expert.id,
        'user': {
            'id': expert.user.id,
            'username': expert.user.username,
            'full_name': expert.user.full_name,
            'location': expert.user.location,
            'reputation': expert.user.reputation_points
        },
        'specializations': expert.specializations.split(',') if expert.specializations else [],
        'credentials': expert.credentials,
        'bio': expert.bio,
        'hourly_rate': expert.hourly_rate,
        'years_experience': expert.years_experience,
        'languages': expert.languages.split(',') if expert.languages else [],
        'consultation_modes': expert.consultation_modes.split(',') if expert.consultation_modes else [],
        'total_consultations': expert.total_consultations,
        'average_rating': expert.average_rating,
        'is_verified': expert.is_verified,
        'reviews': reviews
    })


@expert_bp.route('/<int:expert_id>/availability', methods=['GET'])
def get_availability(expert_id):
    """Get expert availability schedule"""
    expert = ExpertProfile.query.get_or_404(expert_id)
    
    # Get availability slots
    slots = ExpertAvailability.query.filter_by(
        expert_id=expert_id,
        is_active=True
    ).order_by(ExpertAvailability.day_of_week, ExpertAvailability.start_time).all()
    
    availability = {}
    for slot in slots:
        day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][slot.day_of_week]
        if day_name not in availability:
            availability[day_name] = []
        availability[day_name].append({
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M')
        })
    
    # Get upcoming booked slots for next 30 days
    start_date = date.today()
    end_date = start_date + timedelta(days=30)
    
    booked_slots = ConsultationBooking.query.filter(
        and_(
            ConsultationBooking.expert_id == expert_id,
            ConsultationBooking.booking_date >= start_date,
            ConsultationBooking.booking_date <= end_date,
            ConsultationBooking.status.in_(['pending', 'confirmed'])
        )
    ).all()
    
    booked = [{
        'date': booking.booking_date.isoformat(),
        'start_time': booking.start_time.strftime('%H:%M'),
        'end_time': booking.end_time.strftime('%H:%M')
    } for booking in booked_slots]
    
    return jsonify({
        'availability': availability,
        'booked_slots': booked
    })


@expert_bp.route('/register', methods=['POST'])
@login_required
def register_expert():
    """Register as expert"""
    if current_user.is_expert:
        return jsonify({'error': 'Already registered as expert'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['specializations', 'credentials', 'bio', 'hourly_rate', 'years_experience']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    expert_profile = ExpertProfile(
        user_id=current_user.id,
        specializations=data['specializations'],
        credentials=data['credentials'],
        bio=data['bio'],
        hourly_rate=float(data['hourly_rate']),
        years_experience=int(data['years_experience']),
        languages=data.get('languages', 'English'),
        consultation_modes=data.get('consultation_modes', 'video,phone,chat')
    )
    
    current_user.is_expert = True
    db.session.add(expert_profile)
    db.session.commit()
    
    return jsonify({'id': expert_profile.id, 'message': 'Expert profile created successfully'}), 201


@expert_bp.route('/profile', methods=['PUT'])
@login_required
def update_expert_profile():
    """Update expert profile"""
    if not current_user.is_expert:
        return jsonify({'error': 'Not registered as expert'}), 403
    
    expert = ExpertProfile.query.filter_by(user_id=current_user.id).first()
    if not expert:
        return jsonify({'error': 'Expert profile not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'specializations' in data:
        expert.specializations = data['specializations']
    if 'credentials' in data:
        expert.credentials = data['credentials']
    if 'bio' in data:
        expert.bio = data['bio']
    if 'hourly_rate' in data:
        expert.hourly_rate = float(data['hourly_rate'])
    if 'years_experience' in data:
        expert.years_experience = int(data['years_experience'])
    if 'languages' in data:
        expert.languages = data['languages']
    if 'consultation_modes' in data:
        expert.consultation_modes = data['consultation_modes']
    if 'is_available' in data:
        expert.is_available = bool(data['is_available'])
    
    db.session.commit()
    
    return jsonify({'message': 'Profile updated successfully'})


@expert_bp.route('/bookings', methods=['POST'])
@login_required
def create_booking():
    """Create new booking"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['expert_id', 'booking_date', 'start_time', 'end_time', 'mode']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    expert = ExpertProfile.query.get_or_404(data['expert_id'])
    
    # Parse date and time
    booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
    start_time = datetime.strptime(data['start_time'], '%H:%M').time()
    end_time = datetime.strptime(data['end_time'], '%H:%M').time()
    
    # Check if slot is available
    existing_booking = ConsultationBooking.query.filter(
        and_(
            ConsultationBooking.expert_id == expert.id,
            ConsultationBooking.booking_date == booking_date,
            ConsultationBooking.status.in_(['pending', 'confirmed']),
            or_(
                and_(
                    ConsultationBooking.start_time <= start_time,
                    ConsultationBooking.end_time > start_time
                ),
                and_(
                    ConsultationBooking.start_time < end_time,
                    ConsultationBooking.end_time >= end_time
                )
            )
        )
    ).first()
    
    if existing_booking:
        return jsonify({'error': 'Time slot not available'}), 400
    
    # Calculate payment amount (hourly rate * duration in hours)
    duration_hours = (datetime.combine(date.today(), end_time) - 
                     datetime.combine(date.today(), start_time)).seconds / 3600
    payment_amount = expert.hourly_rate * duration_hours
    
    booking = ConsultationBooking(
        expert_id=expert.id,
        farmer_id=current_user.id,
        booking_date=booking_date,
        start_time=start_time,
        end_time=end_time,
        mode=data['mode'],
        issue_description=data.get('issue_description'),
        crop_type=data.get('crop_type'),
        urgency=data.get('urgency', 'medium'),
        payment_amount=payment_amount
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({
        'id': booking.id,
        'payment_amount': payment_amount,
        'message': 'Booking created successfully'
    }), 201


@expert_bp.route('/bookings', methods=['GET'])
@login_required
def get_bookings():
    """Get user's bookings"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    status = request.args.get('status')  # pending, confirmed, completed, cancelled
    
    # Get bookings as farmer or expert
    if current_user.is_expert:
        expert = ExpertProfile.query.filter_by(user_id=current_user.id).first()
        if expert:
            query = ConsultationBooking.query.filter_by(expert_id=expert.id)
        else:
            query = ConsultationBooking.query.filter_by(farmer_id=current_user.id)
    else:
        query = ConsultationBooking.query.filter_by(farmer_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    query = query.order_by(ConsultationBooking.booking_date.desc(), 
                          ConsultationBooking.start_time.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    bookings = []
    for booking in pagination.items:
        bookings.append({
            'id': booking.id,
            'expert': {
                'id': booking.expert.id,
                'user': {
                    'full_name': booking.expert.user.full_name,
                    'username': booking.expert.user.username
                },
                'specializations': booking.expert.specializations.split(',')
            },
            'farmer': {
                'id': booking.farmer.id,
                'name': booking.farmer.full_name
            },
            'booking_date': booking.booking_date.isoformat(),
            'start_time': booking.start_time.strftime('%H:%M'),
            'end_time': booking.end_time.strftime('%H:%M'),
            'mode': booking.mode,
            'status': booking.status,
            'payment_amount': booking.payment_amount,
            'payment_status': booking.payment_status,
            'has_review': booking.review is not None,
            'created_at': booking.created_at.isoformat()
        })
    
    return jsonify({
        'bookings': bookings,
        'pagination': {
            'page': page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })


@expert_bp.route('/bookings/<int:booking_id>', methods=['GET'])
@login_required
def get_booking(booking_id):
    """Get booking details"""
    booking = ConsultationBooking.query.get_or_404(booking_id)
    
    # Check authorization
    expert = ExpertProfile.query.filter_by(user_id=current_user.id).first()
    if booking.farmer_id != current_user.id and (not expert or booking.expert_id != expert.id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'id': booking.id,
        'expert': {
            'id': booking.expert.id,
            'name': booking.expert.user.full_name,
            'specializations': booking.expert.specializations.split(',')
        },
        'farmer': {
            'id': booking.farmer.id,
            'name': booking.farmer.full_name,
            'location': booking.farmer.location
        },
        'booking_date': booking.booking_date.isoformat(),
        'start_time': booking.start_time.strftime('%H:%M'),
        'end_time': booking.end_time.strftime('%H:%M'),
        'mode': booking.mode,
        'status': booking.status,
        'issue_description': booking.issue_description,
        'crop_type': booking.crop_type,
        'urgency': booking.urgency,
        'payment_amount': booking.payment_amount,
        'payment_status': booking.payment_status,
        'expert_notes': booking.expert_notes,
        'created_at': booking.created_at.isoformat()
    })


@expert_bp.route('/bookings/<int:booking_id>/status', methods=['PUT'])
@login_required
def update_booking_status(booking_id):
    """Update booking status (expert only)"""
    booking = ConsultationBooking.query.get_or_404(booking_id)
    
    expert = ExpertProfile.query.filter_by(user_id=current_user.id).first()
    if not expert or booking.expert_id != expert.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['pending', 'confirmed', 'completed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
    
    booking.status = new_status
    
    if 'expert_notes' in data:
        booking.expert_notes = data['expert_notes']
    
    if new_status == 'completed':
        expert.total_consultations += 1
    
    db.session.commit()
    
    return jsonify({'message': 'Booking status updated'})


@expert_bp.route('/bookings/<int:booking_id>/review', methods=['POST'])
@login_required
def add_review(booking_id):
    """Add review for completed booking"""
    booking = ConsultationBooking.query.get_or_404(booking_id)
    
    # Check authorization (farmer only)
    if booking.farmer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if booking.status != 'completed':
        return jsonify({'error': 'Can only review completed consultations'}), 400
    
    if booking.review:
        return jsonify({'error': 'Review already exists'}), 400
    
    data = request.get_json()
    
    if 'rating' not in data or not (1 <= data['rating'] <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    review = ConsultationReview(
        booking_id=booking_id,
        rating=data['rating'],
        review_text=data.get('review_text'),
        would_recommend=data.get('would_recommend', True)
    )
    
    db.session.add(review)
    
    # Update expert rating
    booking.expert.update_rating()
    
    # Add reputation to expert
    booking.expert.user.add_reputation(
        current_app.config.get('POINTS_EXPERT_REVIEW', 15),
        'expert_review_received',
        review.id
    )
    
    db.session.commit()
    
    return jsonify({'id': review.id, 'message': 'Review submitted successfully'}), 201
