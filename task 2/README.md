# University Management System

A comprehensive Django + React web application for managing students, professors, subjects, and faculties with three separate dashboards for different user roles.

## Features

- **Three User Roles & Dashboards**
  - Administrator Dashboard: View all statistics and manage the system
  - Professor Dashboard: View assigned subjects and students
  - Student Dashboard: View enrolled subjects and GPA

- **Five Core Models**
  - Administrator
  - Professor
  - Student
  - Subject
  - Faculty (Computer Science & English departments)

- **Authentication & Security**
  - Django built-in authentication system
  - CORS configuration for API security
  - Protected routes requiring authentication

- **Database**
  - SQLite database with proper relationships
  - OOP principles with DRY (Don't Repeat Yourself) approach
  - Abstract base model for common fields

- **API**
  - RESTful API using Django REST Framework
  - Dashboard endpoints for each user role
  - CRUD operations for all models

## Project Structure

```
task 2/
├── manage.py
├── db.sqlite3
├── create_users.py
├── university_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── university/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── AdminDashboard.jsx
    │   │   ├── ProfessorDashboard.jsx
    │   │   └── StudentDashboard.jsx
    │   ├── services/
    │   │   └── api.js
    │   ├── styles/
    │   │   ├── Auth.css
    │   │   └── Dashboard.css
    │   ├── App.jsx
    │   ├── App.css
    │   ├── index.js
    │   └── index.css
    └── package.json
```

## Installation & Setup

### Backend Setup (Django)

1. **Install Python dependencies:**
   ```bash
   pip install django djangorestframework django-cors-headers python-decouple
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create initial users and data:**
   ```bash
   python create_users.py
   ```

4. **Start Django development server:**
   ```bash
   python manage.py runserver
   ```

   The backend will be available at `http://localhost:8000`

### Frontend Setup (React)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start React development server:**
   ```bash
   npm start
   ```

   The frontend will open at `http://localhost:3000`

## Test Credentials

After running `create_users.py`, use these credentials to login:

- **Admin**
  - Username: `admin`
  - Password: `admin123`
  - Access: Admin Dashboard

- **Professor**
  - Username: `professor1`
  - Password: `prof123`
  - Access: Professor Dashboard

- **Student**
  - Username: `student1`
  - Password: `student123`
  - Access: Student Dashboard

## Django Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/`

Use admin credentials:
- Username: `admin`
- Password: `admin123`

## API Endpoints

### Authentication
- `POST /api/login/` - User login

### Dashboards
- `GET /api/admin-dashboard/` - Admin dashboard data
- `GET /api/professor-dashboard/` - Professor dashboard data
- `GET /api/student-dashboard/` - Student dashboard data

### Resources (RESTful)
- `GET /api/faculties/` - List all faculties
- `GET /api/subjects/` - List all subjects
- `GET /api/professors/` - List all professors
- `GET /api/students/` - List all students
- `GET /api/administrators/` - List all administrators

## Database Models

### Faculty
- name: CharField
- department: CharField (CS or EN)
- description: TextField
- created_at, updated_at, is_active

### Subject
- name: CharField
- code: CharField (unique)
- description: TextField
- faculty: ForeignKey
- credits: IntegerField
- created_at, updated_at, is_active

### Administrator
- user: OneToOneField (User)
- phone: CharField
- office_location: CharField
- created_at, updated_at, is_active

### Professor
- user: OneToOneField (User)
- faculty: ForeignKey
- specialization: CharField
- phone: CharField
- office_hours: CharField
- subjects: ManyToManyField
- created_at, updated_at, is_active

### Student
- user: OneToOneField (User)
- enrollment_number: CharField (unique)
- faculty: ForeignKey
- date_of_birth: DateField
- phone: CharField
- subjects: ManyToManyField
- gpa: DecimalField
- created_at, updated_at, is_active

## CORS Configuration

The application is configured to accept requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

To add more origins, modify `CORS_ALLOWED_ORIGINS` in `university_project/settings.py`

## Deployment to PythonAnywhere (Free Tier)

### Step 1: Create PythonAnywhere Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account

### Step 2: Upload Project Files
1. In PythonAnywhere, go to **Files**
2. Create a new directory for your project
3. Upload all Django files (except frontend)

### Step 3: Create Virtual Environment
1. In **Consoles**, start a Bash console
2. Create virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 mysite
   pip install django djangorestframework django-cors-headers
   ```

### Step 4: Configure Web App
1. Go to **Web** tab
2. Click "Add a new web app"
3. Choose "Manual configuration" and Python 3.9
4. Update WSGI file to point to your project

### Step 5: Configure Settings for Production
In `university_project/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
STATIC_ROOT = '/home/yourusername/mysite/static'
STATIC_URL = '/static/'

# Update CORS for production
CORS_ALLOWED_ORIGINS = [
    "https://yourusername.pythonanywhere.com",
    "http://yourusername.pythonanywhere.com",
]
```

### Step 6: Run Migrations
```bash
python manage.py migrate
python create_users.py
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 8: Reload Web App
In **Web** tab, click the reload button

Your application will be available at `https://yourusername.pythonanywhere.com`

## Development Notes

- The application uses abstract base model for common fields to follow DRY principle
- All API endpoints require authentication (except login)
- CORS is configured to prevent unauthorized API access
- The frontend uses React Router for navigation
- Protected routes ensure only authenticated users can access dashboards

## Troubleshooting

### CORS Errors
If you see CORS errors in the browser console:
1. Ensure Django is running on `http://localhost:8000`
2. Ensure React is running on `http://localhost:3000`
3. Check CORS_ALLOWED_ORIGINS in settings.py

### 404 Errors on API Calls
1. Ensure Django server is running
2. Check URL patterns in `university_project/urls.py`
3. Verify all app URLs are properly included

### Database Errors
1. Run `python manage.py migrate`
2. Ensure db.sqlite3 file has proper permissions
3. Check database configuration in settings.py

## Support

For issues or questions, refer to:
- Django Documentation: https://docs.djangoproject.com
- React Documentation: https://react.dev
- Django REST Framework: https://www.django-rest-framework.org
