"""
Setup Verification Script
Checks if the application is properly configured and ready to run
"""

import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_project.settings')
django.setup()

from django.contrib.auth.models import User
from university.models import Faculty, Subject, Administrator, Professor, Student

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print("✓ Python version OK:", f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("✗ Python 3.9+ required")
        return False

def check_packages():
    """Check if required packages are installed"""
    required_packages = ['django', 'rest_framework', 'corsheaders']
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} NOT installed")
            all_installed = False
    
    return all_installed

def check_database():
    """Check if database exists and has data"""
    try:
        user_count = User.objects.count()
        admin_count = Administrator.objects.count()
        prof_count = Professor.objects.count()
        student_count = Student.objects.count()
        faculty_count = Faculty.objects.count()
        subject_count = Subject.objects.count()
        
        print("\n✓ Database Connected")
        print(f"  - Users: {user_count}")
        print(f"  - Administrators: {admin_count}")
        print(f"  - Professors: {prof_count}")
        print(f"  - Students: {student_count}")
        print(f"  - Faculties: {faculty_count}")
        print(f"  - Subjects: {subject_count}")
        
        if user_count < 3:
            print("\n⚠ Warning: Expected 3+ users. Run 'python create_users.py'")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Database Error: {e}")
        return False

def check_test_users():
    """Check if test users exist"""
    test_users = ['admin', 'professor1', 'student1']
    all_exist = True
    
    print("\n✓ Checking test users:")
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            print(f"  ✓ {username} ({user.email})")
        except User.DoesNotExist:
            print(f"  ✗ {username} NOT FOUND")
            all_exist = False
    
    return all_exist

def check_project_structure():
    """Check if all required files and directories exist"""
    required_paths = [
        'manage.py',
        'requirements.txt',
        'README.md',
        'DEPLOYMENT.md',
        'QUICKSTART.md',
        'db.sqlite3',
        'university/',
        'university_project/',
        'frontend/',
        'frontend/src/',
        'frontend/public/',
    ]
    
    all_exist = True
    print("\n✓ Project Structure:")
    for path in required_paths:
        if Path(path).exists():
            print(f"  ✓ {path}")
        else:
            print(f"  ✗ {path} MISSING")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("University Management System - Setup Verification")
    print("=" * 60)
    print()
    
    checks = {
        "Python Version": check_python_version(),
        "Required Packages": check_packages(),
        "Project Structure": check_project_structure(),
        "Database": check_database(),
        "Test Users": check_test_users(),
    }
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check_name}")
    
    print("=" * 60)
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("\n✓ All checks passed! Ready to start development.")
        print("\nStart the application with:")
        print("  1. Backend: python manage.py runserver")
        print("  2. Frontend: cd frontend && npm start")
        print("\nAccess at: http://localhost:3000")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        if not checks["Required Packages"]:
            print("  Run: pip install -r requirements.txt")
        if not checks["Database"]:
            print("  Run: python manage.py migrate")
        if not checks["Test Users"]:
            print("  Run: python create_users.py")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ Verification Error: {e}")
        sys.exit(1)
