# Crop Doctor - Community Edition

## 🌾 Overview

An integrated agricultural platform combining crop recommendation, disease detection, community forum, and expert consultation features.

## ✨ Features

### Existing Features
- **Crop Recommendation**: ML-based crop suggestions based on soil and climate data
- **Disease Detection**: Image-based plant disease identification
- **Weather Integration**: Real-time weather data
- **PDF Reports**: Downloadable diagnostic reports

### New Community Features
- **Forum System**: 
  - Discussion categories (Crop Management, Pest Control, Irrigation, etc.)
  - Post creation with rich text
  - Comments and nested replies
  - Voting system (upvote/downvote)
  - Location-based filtering
  - Search functionality
  - Content moderation

- **Expert Consultation**:
  - Expert directory with profiles
  - Booking system with calendar
  - Multiple consultation modes (video, phone, chat, in-person)
  - Reviews and ratings
  - Availability management
  - Payment integration (placeholder)

- **User System**:
  - Registration and authentication
  - User profiles
  - Reputation points and badges
  - Activity tracking

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "e:\crop and disease reccommendation\Crop-Recommendation-and-Disease-Detection-System"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If you encounter errors, install packages individually:
   ```bash
   pip install flask==3.0.3 flask-login==0.6.3 flask-sqlalchemy==3.1.1
   pip install python-dotenv==1.0.0 bcrypt==4.1.2 bleach==6.1.0
   pip install numpy pandas scikit-learn pillow requests
   ```

3. **Initialize the database**:
   ```bash
   python database_setup.py
   ```

   This will create:
   - `community.db` - Database with all tables
   - Sample users (admin, farmer, expert)
   - Forum categories
   - Sample expert profile

4. **Run the application**:
   ```bash
   python app_community.py
   ```

5. **Access the application**:
   Open your browser and go to: `http://localhost:5000`

## 👤 Sample Login Credentials

After running `database_setup.py`, you can log in with:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Farmer | `john_farmer` | `farmer123` |
| Expert | `dr_sarah` | `expert123` |

**⚠️ IMPORTANT**: Change these passwords in production!

## 📁 Project Structure

```
Crop-Recommendation-and-Disease-Detection-System/
├── app.py                      # Original app (crop/disease detection)
├── app_community.py            # New integrated app with community features
├── community_models.py         # Database models (SQLAlchemy)
├── database_setup.py           # Database initialization script
├── forum_api.py                # Forum API endpoints
├── expert_api.py               # Expert consultation API endpoints
├── history.py                  # Detection history module
├── pdf_generator.py            # PDF report generation
├── weather.py                  # Weather data integration
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── community.db                # SQLite database (created after setup)
├── templates/
│   ├── auth/
│   │   ├── login.html         # Login page
│   │   └── register.html      # Registration page
│   ├── forum.html             # Forum homepage
│   ├── experts.html           # Expert directory
│   └── index.html             # Main dashboard
├── uploads/                    # Uploaded images
└── models/                     # ML models
```

## 🔧 Configuration

Edit `.env` file to configure:

```env
# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database
SQLALCHEMY_DATABASE_URI=sqlite:///community.db

# File Upload
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads

# Pagination
POSTS_PER_PAGE=20
EXPERTS_PER_PAGE=12

# Reputation Points
POINTS_POST_CREATED=5
POINTS_COMMENT_CREATED=2
POINTS_UPVOTE_RECEIVED=10
POINTS_BEST_ANSWER=50
```

## 📡 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Forum
- `GET /api/forum/categories` - List categories
- `GET /api/forum/posts` - List posts (with filters)
- `GET /api/forum/posts/<id>` - Get single post
- `POST /api/forum/posts` - Create post (auth required)
- `POST /api/forum/posts/<id>/comments` - Add comment
- `POST /api/forum/posts/<id>/vote` - Vote on post
- `GET /api/forum/search?q=<query>` - Search posts

### Expert Consultation
- `GET /api/experts` - List experts (with filters)
- `GET /api/experts/<id>` - Get expert profile
- `GET /api/experts/<id>/availability` - Get availability
- `POST /api/experts/register` - Register as expert
- `POST /api/bookings` - Create booking
- `GET /api/bookings` - List user's bookings
- `POST /api/bookings/<id>/review` - Add review

### Existing Features
- `POST /recommend_crop` - Get crop recommendations
- `POST /classify_disease` - Detect plant disease
- `GET /weather_data` - Get weather information
- `GET /history` - Get detection history

## 🎨 Features in Detail

### Forum System

1. **Browse Categories**: 8 pre-defined categories for organizing discussions
2. **Create Posts**: Rich text editor with image upload support
3. **Engage**: Comment, reply, upvote/downvote
4. **Filter**: By category, location, tags
5. **Search**: Full-text search across posts
6. **Reputation**: Earn points for helpful contributions

### Expert Consultation

1. **Find Experts**: Browse verified agricultural experts
2. **View Profiles**: See credentials, specializations, ratings
3. **Check Availability**: Real-time calendar showing available slots
4. **Book Consultation**: Choose date, time, and consultation mode
5. **Leave Reviews**: Rate and review after consultation
6. **Track Bookings**: View upcoming and past consultations

## 🛠️ Development

### Running in Development Mode

```bash
# Set environment to development
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows

# Run with auto-reload
python app_community.py
```

### Database Migrations

To reset the database:
```bash
# Delete existing database
rm community.db  # Linux/Mac
del community.db  # Windows

# Reinitialize
python database_setup.py
```

## 📊 Database Schema

The system uses SQLite with the following main tables:

- **users** - User accounts and authentication
- **user_profiles** - Extended user information
- **forum_categories** - Forum categories
- **forum_posts** - Forum posts/questions
- **forum_comments** - Comments and replies
- **post_votes** - Upvotes/downvotes on posts
- **expert_profiles** - Expert credentials and info
- **expert_availability** - Expert schedule
- **consultation_bookings** - Booking appointments
- **consultation_reviews** - Expert reviews and ratings
- **reputation_logs** - Reputation point history

## 🔒 Security Notes

1. **Change Default Passwords**: Update sample user passwords immediately
2. **Secret Key**: Generate a strong SECRET_KEY for production
3. **HTTPS**: Use HTTPS in production
4. **Input Validation**: All user inputs are sanitized
5. **SQL Injection**: Using SQLAlchemy ORM prevents SQL injection
6. **XSS Protection**: HTML content is sanitized with bleach

## 🚀 Production Deployment

For production deployment:

1. **Use PostgreSQL** instead of SQLite:
   ```env
   SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost/dbname
   ```

2. **Use a production server** (Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app_community:app
   ```

3. **Enable HTTPS** with SSL certificates

4. **Set up email notifications** (configure SMTP in `.env`)

5. **Consider cloud storage** for uploaded images (AWS S3, Cloudinary)

6. **Add caching** (Redis) for better performance

## 🐛 Troubleshooting

### ModuleNotFoundError
```bash
# Install missing package
pip install <package-name>
```

### Database Errors
```bash
# Reset database
python database_setup.py
```

### Port Already in Use
```python
# Change port in app_community.py
app.run(debug=True, port=5001)  # Use different port
```

### TensorFlow Not Available
The system works without TensorFlow using color-based disease detection. To enable ML-based detection, install TensorFlow and place the trained model in `models/` directory.

## 📝 License

This project is for educational and agricultural support purposes.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Mobile app development
- Real-time chat for consultations
- Payment gateway integration
- Multi-language support
- Advanced search with Elasticsearch
- Video consultation integration

## 📞 Support

For issues or questions:
1. Check this README
2. Review the implementation plan in artifacts
3. Check the API documentation above

## 🎯 Next Steps

1. **Test the System**: Log in with sample credentials and explore features
2. **Customize**: Update categories, add more experts, customize UI
3. **Integrate Payment**: Add Stripe or M-Pesa for paid consultations
4. **Deploy**: Follow production deployment guide
5. **Monitor**: Set up logging and monitoring

---

**Built with ❤️ for farmers and agricultural communities**
