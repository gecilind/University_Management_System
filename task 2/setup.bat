@echo off
REM University Management System - Setup Script
REM This script sets up the complete development environment

echo.
echo ========================================
echo University Management System Setup
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+
    exit /b 1
)
python --version

REM Check Node.js
echo.
echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 14+
    exit /b 1
)
node --version

REM Install Python dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

REM Run Django migrations
echo.
echo Running Django migrations...
python manage.py migrate

REM Create test users
echo.
echo Creating test users...
python create_users.py

REM Install frontend dependencies
echo.
echo Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo 1. Backend (Django):
echo    python manage.py runserver
echo.
echo 2. Frontend (React) - In another terminal:
echo    cd frontend
echo    npm start
echo.
echo Access the application at: http://localhost:3000
echo Admin Panel at: http://localhost:8000/admin/
echo.
echo Test Credentials:
echo   Admin:     admin / admin123
echo   Professor: professor1 / prof123
echo   Student:   student1 / student123
echo.
