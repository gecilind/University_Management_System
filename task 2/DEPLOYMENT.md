# University Management System - Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Testing the Application](#testing-the-application)
3. [Deploying to PythonAnywhere](#deploying-to-pythonanywhere)

## Local Development Setup

### Prerequisites
- Python 3.9 or higher
- Node.js 14 or higher
- Git (optional)

### Step 1: Clone/Download the Project

Navigate to your project directory:
```bash
cd "C:\Users\LindGeci\Desktop\task 2"
```

### Step 2: Backend Setup

Install required Python packages:
```bash
pip install -r requirements.txt
```

Run migrations to setup the database:
```bash
python manage.py migrate
```

Create initial users and test data:
```bash
python create_users.py
```

Start the Django development server:
```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
```

Keep this terminal open.

### Step 3: Frontend Setup

Open a new terminal/command prompt and navigate to the frontend folder:
```bash
cd frontend
```

Install Node dependencies:
```bash
npm install
```

Start the React development server:
```bash
npm start
```

The frontend will automatically open in your browser at `http://localhost:3000`

## Testing the Application

### Access Points

1. **Django Admin Panel**: `http://localhost:8000/admin/`
   - Username: `admin`
   - Password: `admin123`

2. **React Application**: `http://localhost:3000/`
   - Automatic login redirects to dashboard based on user role

### Test Scenarios

#### 1. Admin Dashboard
1. At login page, enter:
   - Username: `admin`
   - Password: `admin123`
2. Click "Login"
3. You should see Admin Dashboard with:
   - Total Students, Professors, Subjects, Faculties statistics
   - Faculty overview table
   - Recent enrollments table

#### 2. Professor Dashboard
1. At login page, enter:
   - Username: `professor1`
   - Password: `prof123`
2. Click "Login"
3. You should see Professor Dashboard with:
   - Professor profile information
   - Teaching subjects and students count
   - List of assigned subjects

#### 3. Student Dashboard
1. At login page, enter:
   - Username: `student1`
   - Password: `student123`
2. Click "Login"
3. You should see Student Dashboard with:
   - Student profile information
   - Current GPA and enrolled subjects count
   - List of enrolled subjects

### Testing API Endpoints

You can test API endpoints using Postman or curl:

```bash
# Login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Get Admin Dashboard
curl -X GET http://localhost:8000/api/admin-dashboard/ \
  -H "Authorization: Bearer token"

# Get Faculties
curl -X GET http://localhost:8000/api/faculties/ \
  -H "Authorization: Bearer token"
```

## Deploying to PythonAnywhere

### Step 1: Create PythonAnywhere Account

1. Visit https://www.pythonanywhere.com
2. Sign up for a free account
3. Verify your email

### Step 2: Upload Project Files

#### Option A: Using Web Interface
1. Log in to PythonAnywhere
2. Go to "Files" tab
3. Create a new directory: `/home/yourusername/mysite`
4. Upload all files except:
   - `frontend/node_modules/` (will be installed fresh)
   - `__pycache__/` directories
   - `.git/` if applicable

#### Option B: Using Git (Recommended)
1. Set up a GitHub repository for your project
2. In PythonAnywhere Bash console:
   ```bash
   git clone https://github.com/yourusername/university-management.git mysite
   cd mysite
   ```

### Step 3: Set Up Virtual Environment

In PythonAnywhere Bash console:

```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.9 mysite

# Your virtual environment is now activated (you should see (mysite) in the prompt)

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Django Settings

Edit `university_project/settings.py` and modify:

```python
# Change DEBUG to False for production
DEBUG = False

# Add your PythonAnywhere domain
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'www.yourusername.pythonanywhere.com']

# Configure static files
STATIC_ROOT = '/home/yourusername/mysite/static'
STATIC_URL = '/static/'

# Update CORS for production
CORS_ALLOWED_ORIGINS = [
    "https://yourusername.pythonanywhere.com",
    "http://yourusername.pythonanywhere.com",
    "https://www.yourusername.pythonanywhere.com",
    "http://www.yourusername.pythonanywhere.com",
]

# Recommended security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Step 5: Run Migrations and Setup Database

In PythonAnywhere Bash console:

```bash
# Activate your virtual environment
workon mysite

# Navigate to project directory
cd ~/mysite

# Run migrations
python manage.py migrate

# Create users and initial data
python create_users.py

# Collect static files (important for Django admin to work)
python manage.py collectstatic --noinput
```

### Step 6: Configure Web App

1. Go to "Web" tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.9
5. Update the WSGI configuration file:
   - Click on the WSGI file link (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
   - Replace the content with:

```python
import os
import sys

path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'university_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. Save the file

### Step 7: Configure Virtual Environment for Web App

1. In the "Web" tab
2. Find "Virtualenv:" section
3. Click and enter the path: `/home/yourusername/.virtualenvs/mysite`

### Step 8: Reload Web App

1. In the "Web" tab, click the green "Reload yourusername.pythonanywhere.com" button
2. Wait a few seconds for the reload to complete

### Step 9: Verify Deployment

1. Visit your site: `https://yourusername.pythonanywhere.com/admin/`
2. Login with admin credentials
3. Verify all features work correctly

### Step 10: Deploy Frontend

For the best experience, you can deploy the React frontend separately or build it and serve it from Django.

#### Option A: Serve React from Django (Recommended for free tier)

1. Build React:
   ```bash
   cd frontend
   npm run build
   ```

2. Copy build folder to Django static files:
   ```bash
   # In your mysite directory
   mkdir -p staticfiles/react
   cp -r frontend/build/* staticfiles/react/
   ```

3. Configure Django to serve React index.html from the root URL

#### Option B: Deploy Frontend Separately

You can deploy the React frontend to:
- Vercel (https://vercel.com) - Free tier available
- Netlify (https://netlify.com) - Free tier available
- GitHub Pages

## Troubleshooting

### Issue: "ModuleNotFoundError" when accessing the site

**Solution**: 
- Verify virtual environment is configured correctly
- Check WSGI configuration file
- Restart the web app

### Issue: Static files not loading (admin interface looks broken)

**Solution**:
- Run `python manage.py collectstatic --noinput` in PythonAnywhere console
- Reload the web app

### Issue: 502 Bad Gateway Error

**Solution**:
- Check error log in PythonAnywhere "Web" tab
- Ensure DEBUG = False is set in settings
- Verify ALLOWED_HOSTS includes your domain

### Issue: Can't login to admin panel

**Solution**:
- Ensure you ran `python create_users.py`
- Check that migrations were run successfully
- Verify database file permissions

### Issue: CORS errors when accessing API

**Solution**:
- Check CORS_ALLOWED_ORIGINS in settings.py
- Ensure your frontend domain is added
- Verify CORS middleware is installed

## Production Checklist

Before going live with your application:

- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Configure CORS_ALLOWED_ORIGINS for your domain
- [ ] Run collectstatic
- [ ] Set secure cookie settings (SECURE_SSL_REDIRECT, etc.)
- [ ] Run all migrations
- [ ] Test all three dashboards
- [ ] Test login functionality
- [ ] Verify API endpoints work
- [ ] Check database backups
- [ ] Monitor error logs

## Monitoring and Maintenance

1. **Check Error Logs**: View "Error log" in PythonAnywhere "Web" tab
2. **Monitor Resources**: Check "CPU and Internet usage" 
3. **Regular Backups**: Download database backup periodically
4. **Update Dependencies**: Periodically check for security updates

## Support Resources

- PythonAnywhere Help: https://help.pythonanywhere.com
- Django Documentation: https://docs.djangoproject.com
- Django REST Framework: https://www.django-rest-framework.org
- React Documentation: https://react.dev
