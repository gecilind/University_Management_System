# Quick Start Guide

## For Windows Users

### 1. Run the Setup Script
Double-click `setup.bat` to automatically install all dependencies and create test users.

The script will:
- Install Python packages
- Run Django migrations
- Create test users and initial data
- Install React dependencies

### 2. Start the Application

**Terminal 1 - Django Backend:**
```powershell
python manage.py runserver
```

**Terminal 2 - React Frontend:**
```powershell
cd frontend
npm start
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Admin Panel**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

### 4. Login with Test Credentials

Choose one of these accounts:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Professor | professor1 | prof123 |
| Student | student1 | student123 |

---

## For Mac/Linux Users

### 1. Run Setup Commands

```bash
# Navigate to project directory
cd "path/to/task 2"

# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create test users
python create_users.py

# Install React dependencies
cd frontend
npm install
cd ..
```

### 2. Start the Application

**Terminal 1:**
```bash
python manage.py runserver
```

**Terminal 2:**
```bash
cd frontend
npm start
```

### 3. Access the Application

Same as above - http://localhost:3000 and http://localhost:8000/admin/

---

## Project Overview

### Backend Structure
```
university_project/      # Django project settings
  ├── settings.py       # Django configuration
  ├── urls.py           # Main URL routing
  └── wsgi.py           # WSGI application

university/             # Django app with models, views, and APIs
  ├── models.py         # Database models
  ├── views.py          # API views
  ├── serializers.py    # REST serializers
  ├── urls.py           # App URL routing
  └── admin.py          # Admin configuration
```

### Frontend Structure
```
frontend/
  ├── public/
  │   └── index.html    # Main HTML file
  ├── src/
  │   ├── pages/        # Page components
  │   ├── services/     # API communication
  │   ├── styles/       # CSS stylesheets
  │   ├── App.jsx       # Main App component
  │   └── index.js      # React entry point
  └── package.json      # Dependencies
```

---

## Key Features Implemented

✅ **5 Core Models:**
- Administrator
- Professor
- Student
- Subject
- Faculty (Computer Science & English)

✅ **3 Dashboards:**
- Admin Dashboard (view statistics)
- Professor Dashboard (view assigned subjects)
- Student Dashboard (view enrolled subjects)

✅ **Authentication:**
- Django built-in auth system
- Protected routes
- Login/Logout functionality

✅ **API:**
- RESTful endpoints
- CORS configured
- All operations secured

✅ **Database:**
- SQLite (development)
- Proper relationships
- OOP principles (DRY)

---

## Troubleshooting

### Port Already in Use

If port 8000 or 3000 is already in use:

**Django (port 8000):**
```bash
python manage.py runserver 8001
```

**React (port 3000):**
```bash
cd frontend
PORT=3001 npm start
```

### Database Issues

Reset the database:
```bash
# Remove old database
del db.sqlite3

# Recreate database
python manage.py migrate
python create_users.py
```

### Module Not Found Error

Reinstall dependencies:
```bash
# Python
pip install -r requirements.txt

# Node
cd frontend
npm install
```

---

## Next Steps

1. **Test the Application:**
   - Login with each user type
   - Navigate through each dashboard
   - Check the Django admin panel

2. **Explore the Admin Panel:**
   - Visit http://localhost:8000/admin/
   - Login with admin credentials
   - View and manage all models

3. **Deploy to PythonAnywhere:**
   - See `DEPLOYMENT.md` for detailed instructions
   - Free tier account at pythonanywhere.com
   - Follow the step-by-step guide

4. **Customize:**
   - Add more users via Django admin
   - Modify dashboard layouts
   - Add additional subjects and faculty

---

## Important Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management utility |
| `create_users.py` | Script to create test users |
| `requirements.txt` | Python dependencies |
| `README.md` | Detailed documentation |
| `DEPLOYMENT.md` | Deployment instructions |
| `setup.bat` | Automated setup for Windows |

---

## Support

For detailed documentation, see:
- `README.md` - Full documentation
- `DEPLOYMENT.md` - Deployment guide
- Django Docs: https://docs.djangoproject.com
- React Docs: https://react.dev

Happy coding! 🚀
