@echo off
echo ============================================================
echo  CROP DOCTOR - COMMUNITY EDITION SETUP
echo ============================================================
echo.

echo Step 1: Installing Python dependencies...
echo.
pip install flask==3.0.3 flask-login==0.6.3 flask-sqlalchemy==3.1.1
pip install python-dotenv==1.0.0 bcrypt==4.1.2 bleach==6.1.0 markdown==3.5.1
pip install numpy pandas scikit-learn pillow requests fpdf2

echo.
echo Step 2: Initializing database...
echo.
python database_setup.py

echo.
echo ============================================================
echo  SETUP COMPLETE!
echo ============================================================
echo.
echo Sample Login Credentials:
echo   Admin:  username='admin'      password='admin123'
echo   Farmer: username='john_farmer' password='farmer123'
echo   Expert: username='dr_sarah'    password='expert123'
echo.
echo To start the application, run:
echo   python app_community.py
echo.
echo Then open your browser to: http://localhost:5000
echo ============================================================
pause
