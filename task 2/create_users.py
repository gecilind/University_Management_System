"""
Script to create initial users and data for the University application
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_project.settings')
django.setup()

from django.contrib.auth.models import User
from university.models import Faculty, Subject, Administrator, Professor, Student

# Clear existing data (optional)
# User.objects.all().delete()
# Faculty.objects.all().delete()

print("Creating Faculty data...")
# Create faculties
cs_faculty, _ = Faculty.objects.get_or_create(
    department='CS',
    defaults={'name': 'Computer Science Faculty', 'description': 'Faculty of Computer Science and Engineering'}
)

en_faculty, _ = Faculty.objects.get_or_create(
    department='EN',
    defaults={'name': 'English Faculty', 'description': 'Faculty of English and Language Studies'}
)

print("Creating Subjects...")
# Create subjects for Computer Science
subjects_cs = [
    {'name': 'Data Structures', 'code': 'CS101', 'faculty': cs_faculty, 'credits': 4},
    {'name': 'Web Development', 'code': 'CS102', 'faculty': cs_faculty, 'credits': 3},
    {'name': 'Database Management', 'code': 'CS103', 'faculty': cs_faculty, 'credits': 3},
]

for subject_data in subjects_cs:
    Subject.objects.get_or_create(code=subject_data['code'], defaults=subject_data)

# Create subjects for English
subjects_en = [
    {'name': 'English Literature', 'code': 'EN101', 'faculty': en_faculty, 'credits': 3},
    {'name': 'Creative Writing', 'code': 'EN102', 'faculty': en_faculty, 'credits': 3},
    {'name': 'Linguistics', 'code': 'EN103', 'faculty': en_faculty, 'credits': 3},
]

for subject_data in subjects_en:
    Subject.objects.get_or_create(code=subject_data['code'], defaults=subject_data)

print("Creating Users and Profiles...")

# Create Admin User
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@university.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print(f"✓ Created Admin User: {admin_user.username}")
else:
    print(f"✓ Admin User already exists: {admin_user.username}")

# Create Administrator Profile
Administrator.objects.get_or_create(
    user=admin_user,
    defaults={'phone': '1234567890', 'office_location': 'Main Building, Room 101'}
)
print("✓ Administrator profile created")

# Create Professor User
prof_user, created = User.objects.get_or_create(
    username='professor1',
    defaults={
        'email': 'professor1@university.com',
        'first_name': 'John',
        'last_name': 'Doe',
    }
)
if created:
    prof_user.set_password('prof123')
    prof_user.save()
    print(f"✓ Created Professor User: {prof_user.username}")
else:
    print(f"✓ Professor User already exists: {prof_user.username}")

# Create Professor Profile
professor, _ = Professor.objects.get_or_create(
    user=prof_user,
    defaults={
        'faculty': cs_faculty,
        'specialization': 'Software Engineering',
        'phone': '9876543210',
        'office_hours': 'Mon-Fri 2:00 PM - 4:00 PM'
    }
)
# Add subjects to professor
cs_subjects = Subject.objects.filter(faculty=cs_faculty)
professor.subjects.set(cs_subjects)
print("✓ Professor profile created with subjects")

# Create Student User
student_user, created = User.objects.get_or_create(
    username='student1',
    defaults={
        'email': 'student1@university.com',
        'first_name': 'Jane',
        'last_name': 'Smith',
    }
)
if created:
    student_user.set_password('student123')
    student_user.save()
    print(f"✓ Created Student User: {student_user.username}")
else:
    print(f"✓ Student User already exists: {student_user.username}")

# Create Student Profile
student, _ = Student.objects.get_or_create(
    user=student_user,
    defaults={
        'enrollment_number': 'STU001',
        'faculty': cs_faculty,
        'phone': '5555555555',
        'gpa': 3.85
    }
)
# Add subjects to student
student.subjects.set(Subject.objects.filter(faculty=cs_faculty)[:2])
print("✓ Student profile created with subjects")

print("\n" + "="*50)
print("SUCCESS! All users and initial data created!")
print("="*50)
print("\nTest Credentials:")
print("Admin      - Username: admin, Password: admin123")
print("Professor  - Username: professor1, Password: prof123")
print("Student    - Username: student1, Password: student123")
print("\nAccess admin panel at: http://localhost:8000/admin/")
