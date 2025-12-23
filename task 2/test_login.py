"""Test login API"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_project.settings')
django.setup()

from django.contrib.auth.models import User

# Test if password is set correctly
admin = User.objects.get(username='admin')
print('Testing admin user:')
print(f'Username: {admin.username}')
print(f'Password check (admin123): {admin.check_password("admin123")}')
print(f'Is staff: {admin.is_staff}')
print(f'Is superuser: {admin.is_superuser}')
print(f'Is active: {admin.is_active}')
print()

# Test other users
prof = User.objects.get(username='professor1')
print('Testing professor1 user:')
print(f'Username: {prof.username}')
print(f'Password check (prof123): {prof.check_password("prof123")}')
print(f'Is active: {prof.is_active}')
print()

stu = User.objects.get(username='student1')
print('Testing student1 user:')
print(f'Username: {stu.username}')
print(f'Password check (student123): {stu.check_password("student123")}')
print(f'Is active: {stu.is_active}')
