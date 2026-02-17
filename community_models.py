"""
Community Features Database Models
SQLAlchemy models for Forum and Expert Consultation System
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ============================================================================
# USER AUTHENTICATION & PROFILES
# ============================================================================

class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    location = db.Column(db.String(100))  # District/Region
    phone = db.Column(db.String(20))
    reputation_points = db.Column(db.Integer, default=0)
    is_expert = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    posts = db.relationship('ForumPost', backref='author', lazy='dynamic', foreign_keys='ForumPost.author_id')
    comments = db.relationship('ForumComment', backref='author', lazy='dynamic')
    expert_profile = db.relationship('ExpertProfile', backref='user', uselist=False)
    bookings_as_farmer = db.relationship('ConsultationBooking', backref='farmer', lazy='dynamic', foreign_keys='ConsultationBooking.farmer_id')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def add_reputation(self, points, action_type, reference_id=None):
        """Add reputation points and log the action"""
        self.reputation_points += points
        log = ReputationLog(
            user_id=self.id,
            points=points,
            action_type=action_type,
            reference_id=reference_id
        )
        db.session.add(log)
    
    def __repr__(self):
        return f'<User {self.username}>'


class UserProfile(db.Model):
    """Extended user profile information"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    expertise_areas = db.Column(db.String(255))  # Comma-separated
    farm_size = db.Column(db.String(50))  # e.g., "5 acres"
    crops_grown = db.Column(db.String(255))  # Comma-separated
    languages = db.Column(db.String(100))  # e.g., "English, Swahili"
    
    user = db.relationship('User', backref=db.backref('profile', uselist=False))


# ============================================================================
# FORUM SYSTEM
# ============================================================================

class ForumCategory(db.Model):
    """Forum categories for organizing posts"""
    __tablename__ = 'forum_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Emoji or icon class
    slug = db.Column(db.String(100), unique=True, nullable=False)
    post_count = db.Column(db.Integer, default=0)
    
    posts = db.relationship('ForumPost', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class ForumPost(db.Model):
    """Forum posts/questions"""
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('forum_categories.id'), nullable=False)
    location = db.Column(db.String(100))  # District/Region
    tags = db.Column(db.String(255))  # Comma-separated tags
    image_url = db.Column(db.String(255))  # Optional image
    views = db.Column(db.Integer, default=0)
    is_solved = db.Column(db.Boolean, default=False)
    is_pinned = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('ForumComment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    votes = db.relationship('PostVote', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    flags = db.relationship('PostFlag', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def vote_count(self):
        """Calculate total vote score"""
        upvotes = PostVote.query.filter_by(post_id=self.id, vote_type='upvote').count()
        downvotes = PostVote.query.filter_by(post_id=self.id, vote_type='downvote').count()
        return upvotes - downvotes
    
    @property
    def comment_count(self):
        """Get total comment count"""
        return self.comments.count()
    
    def __repr__(self):
        return f'<Post {self.title[:30]}>'


class ForumComment(db.Model):
    """Comments on forum posts"""
    __tablename__ = 'forum_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('forum_comments.id'))  # For nested replies
    is_best_answer = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    replies = db.relationship('ForumComment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    votes = db.relationship('CommentVote', backref='comment', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def vote_count(self):
        """Calculate total vote score"""
        upvotes = CommentVote.query.filter_by(comment_id=self.id, vote_type='upvote').count()
        downvotes = CommentVote.query.filter_by(comment_id=self.id, vote_type='downvote').count()
        return upvotes - downvotes
    
    def __repr__(self):
        return f'<Comment {self.id}>'


class PostVote(db.Model):
    """Votes on forum posts"""
    __tablename__ = 'post_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_vote'),)


class CommentVote(db.Model):
    """Votes on comments"""
    __tablename__ = 'comment_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('forum_comments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('comment_id', 'user_id', name='unique_comment_vote'),)


class PostFlag(db.Model):
    """Flagged posts for moderation"""
    __tablename__ = 'post_flags'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, resolved, dismissed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))


# ============================================================================
# EXPERT CONSULTATION SYSTEM
# ============================================================================

class ExpertProfile(db.Model):
    """Expert profile with credentials and specializations"""
    __tablename__ = 'expert_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    specializations = db.Column(db.String(255), nullable=False)  # Comma-separated
    credentials = db.Column(db.Text)  # Degrees, certifications
    bio = db.Column(db.Text)
    hourly_rate = db.Column(db.Float, default=0.0)
    years_experience = db.Column(db.Integer)
    languages = db.Column(db.String(100))  # Languages spoken
    consultation_modes = db.Column(db.String(100))  # video,phone,chat,in-person
    is_verified = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    total_consultations = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    availability = db.relationship('ExpertAvailability', backref='expert', lazy='dynamic', cascade='all, delete-orphan')
    bookings = db.relationship('ConsultationBooking', backref='expert', lazy='dynamic', foreign_keys='ConsultationBooking.expert_id')
    badges = db.relationship('ExpertBadge', backref='expert', lazy='dynamic')
    
    def update_rating(self):
        """Recalculate average rating from reviews"""
        reviews = ConsultationReview.query.join(ConsultationBooking).filter(
            ConsultationBooking.expert_id == self.id
        ).all()
        
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = round(total_rating / len(reviews), 2)
        else:
            self.average_rating = 0.0
    
    def __repr__(self):
        return f'<ExpertProfile {self.user.username}>'


class ExpertAvailability(db.Model):
    """Expert availability schedule"""
    __tablename__ = 'expert_availability'
    
    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer, db.ForeignKey('expert_profiles.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    __table_args__ = (db.UniqueConstraint('expert_id', 'day_of_week', 'start_time', name='unique_availability'),)


class ConsultationBooking(db.Model):
    """Consultation booking/appointment"""
    __tablename__ = 'consultation_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer, db.ForeignKey('expert_profiles.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    mode = db.Column(db.String(20), nullable=False)  # video, phone, chat, in-person
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    issue_description = db.Column(db.Text)
    crop_type = db.Column(db.String(100))
    urgency = db.Column(db.String(20))  # low, medium, high
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    payment_amount = db.Column(db.Float)
    expert_notes = db.Column(db.Text)  # Notes from expert after consultation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    review = db.relationship('ConsultationReview', backref='booking', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Booking {self.id} - {self.status}>'


class ConsultationReview(db.Model):
    """Reviews and ratings for consultations"""
    __tablename__ = 'consultation_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('consultation_bookings.id'), nullable=False, unique=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review_text = db.Column(db.Text)
    would_recommend = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id} - {self.rating} stars>'


class ExpertBadge(db.Model):
    """Badges/achievements for experts"""
    __tablename__ = 'expert_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer, db.ForeignKey('expert_profiles.id'), nullable=False)
    badge_type = db.Column(db.String(50), nullable=False)  # top_rated, verified, specialist, etc.
    badge_name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================================================
# REPUTATION & GAMIFICATION
# ============================================================================

class ReputationLog(db.Model):
    """Log of reputation point changes"""
    __tablename__ = 'reputation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(50), nullable=False)  # post_created, upvote_received, etc.
    reference_id = db.Column(db.Integer)  # ID of related post/comment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='reputation_history')


class UserBadge(db.Model):
    """Badges/achievements for users"""
    __tablename__ = 'user_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_name = db.Column(db.String(100), nullable=False)
    badge_type = db.Column(db.String(50))  # contributor, helper, expert, etc.
    description = db.Column(db.String(255))
    icon = db.Column(db.String(50))
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='badges')


# ============================================================================
# NOTIFICATIONS
# ============================================================================

class Notification(db.Model):
    """User notifications"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))  # comment, booking, upvote, etc.
    reference_id = db.Column(db.Integer)  # ID of related object
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='notifications')
