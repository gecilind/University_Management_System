from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import jwt
import json
from datetime import datetime, timedelta
from django.conf import settings
from .models import Faculty, Subject, Administrator, Professor, Student, Grade, RefreshToken
from .serializers import (
    FacultySerializer, SubjectSerializer, AdministratorSerializer,
    ProfessorSerializer, StudentSerializer, DashboardAdminSerializer,
    DashboardProfessorSerializer, DashboardStudentSerializer, GradeSerializer
)
from .permissions import IsAdmin, IsProfessor, IsStudent


@api_view(['GET'])
@permission_classes([AllowAny])
def get_users(request):
    """Get all users for debugging"""
    users = User.objects.all()
    user_list = []
    
    for user in users:
        role = 'user'
        if hasattr(user, 'administrator'):
            role = 'admin'
        elif hasattr(user, 'professor'):
            role = 'professor'
        elif hasattr(user, 'student'):
            role = 'student'
        
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': role,
            'is_active': user.is_active,
            'is_staff': user.is_staff
        })
    
    return Response({
        'total_users': len(user_list),
        'users': user_list
    })


def _get_user_role(user):
    """Determine user role"""
    if hasattr(user, 'administrator'):
        return 'admin'
    elif hasattr(user, 'professor'):
        return 'professor'
    elif hasattr(user, 'student'):
        return 'student'
    return 'user'


def _create_jwt_token(user, role):
    """Create JWT access token"""
    from django.utils import timezone
    now = timezone.now()
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': role,
        'iat': int(now.timestamp()),
        'exp': int((now + timedelta(minutes=settings.JWT_EXPIRATION_DELTA_MINUTES)).timestamp())
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    # PyJWT returns string in newer versions, ensure it's a string
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def _create_refresh_token(user):
    """Create refresh token and store in database"""
    import secrets
    from django.utils import timezone
    
    # Generate a secure random token (not JWT, just a random string)
    token = secrets.token_urlsafe(64)
    expires_at = timezone.now() + timedelta(days=settings.JWT_REFRESH_EXPIRATION_DELTA_DAYS)
    
    # Store in database
    RefreshToken.objects.create(
        token=token,
        user=user,
        expires_at=expires_at
    )
    
    return token


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login and return JWT access token + refresh token in HttpOnly cookie"""
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_active:
                role = _get_user_role(user)
                
                # Create tokens
                access_token = _create_jwt_token(user, role)
                refresh_token = _create_refresh_token(user)

                # Return JWT in response body and store in cookie
                response = Response({
                    'message': 'Login successful',
                    'access_token': access_token,  # JWT in response body
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': role,
                }, status=status.HTTP_200_OK)

                # Store access token in cookie (not HttpOnly so JS can read it for Authorization header)
                response.set_cookie(
                    'accessToken',
                    access_token,
                    httponly=False,  # Allow JS to read for Authorization header
                    secure=False,  # change to True in production
                    samesite='Lax',
                    max_age=settings.JWT_EXPIRATION_DELTA_MINUTES * 60  # 15 minutes
                )

                # Store refresh token in HttpOnly cookie
                response.set_cookie(
                    'refreshToken',
                    refresh_token,
                    httponly=True,
                    secure=False,  # change to True in production
                    samesite='Lax',
                    max_age=settings.JWT_REFRESH_EXPIRATION_DELTA_DAYS * 24 * 60 * 60  # 1 day
                )

                return response
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'message': 'Use POST with username and password'})


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """Logout: remove refresh token from DB and delete cookie"""
    refresh_token = request.COOKIES.get('refreshToken')
    
    if refresh_token:
        # Remove refresh token from database
        try:
            RefreshToken.objects.filter(token=refresh_token).delete()
        except Exception:
            pass  # Token might not exist, continue anyway
    
    # Delete both access token and refresh token cookies
    response = Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
    response.delete_cookie('accessToken')
    response.delete_cookie('refreshToken')
    return response


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def renew_token_view(request):
    """Renew: read refresh token from cookie, validate against DB, return new JWT in response body"""
    refresh_token = request.COOKIES.get('refreshToken')
    
    if not refresh_token:
        return Response({'error': 'Missing refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Validate refresh token against database
        refresh_token_obj = RefreshToken.objects.get(token=refresh_token)
        
        # Check if token is expired
        from django.utils import timezone
        if refresh_token_obj.expires_at < timezone.now():
            # Delete expired token
            refresh_token_obj.delete()
            return Response({'error': 'Refresh token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = refresh_token_obj.user
        
        if not user.is_active:
            return Response({'error': 'User is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get user role and create new JWT with SAME payload/claims
        role = _get_user_role(user)
        access_token = _create_jwt_token(user, role)

        # Return new JWT in response body and store in cookie
        response = Response({
            'message': 'Token renewed',
            'access_token': access_token  # JWT in response body
        }, status=status.HTTP_200_OK)
        
        # Store new access token in cookie
        response.set_cookie(
            'accessToken',
            access_token,
            httponly=False,  # Allow JS to read for Authorization header
            secure=False,  # change to True in production
            samesite='Lax',
            max_age=settings.JWT_EXPIRATION_DELTA_MINUTES * 60  # 15 minutes
        )
        
        return response
    
    except RefreshToken.DoesNotExist:
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': f'Token renewal failed: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def admin_dashboard(request):
    """Get admin dashboard data - Admin only"""
    data = {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_professors': Professor.objects.filter(is_active=True).count(),
        'total_subjects': Subject.objects.filter(is_active=True).count(),
        'total_faculties': Faculty.objects.filter(is_active=True).count(),
        'recent_enrollments': Student.objects.filter(is_active=True).order_by('-created_at')[:5]
    }
    
    serializer = DashboardAdminSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsProfessor])
def professor_dashboard(request):
    """Get professor dashboard data - Professor only"""
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        return Response({'error': 'Professor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    subjects = professor.subjects.all()
    # Get all students enrolled in any of the professor's subjects
    students = Student.objects.filter(subjects__in=subjects, is_active=True).distinct()
    students_count = students.count()
    
    data = {
        'professor': professor,
        'subjects': subjects,
        'students': students,
        'students_count': students_count
    }
    
    serializer = DashboardProfessorSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def student_dashboard(request):
    """Get student dashboard data - Student only"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    enrolled_subjects = student.subjects.all()
    
    data = {
        'student': student,
        'enrolled_subjects': enrolled_subjects,
        'gpa': student.gpa
    }
    
    serializer = DashboardStudentSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def student_courses(request):
    """Get all available courses for student - shows enrolled status"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get all active subjects
    all_subjects = Subject.objects.filter(is_active=True)
    
    # Get enrolled subject IDs
    enrolled_subject_ids = set(student.subjects.filter(is_active=True).values_list('id', flat=True))
    
    # Serialize subjects with enrollment status
    courses_data = []
    for subject in all_subjects:
        subject_data = SubjectSerializer(subject).data
        subject_data['is_enrolled'] = subject.id in enrolled_subject_ids
        courses_data.append(subject_data)
    
    return Response({
        'courses': courses_data,
        'total_courses': len(courses_data),
        'enrolled_count': len(enrolled_subject_ids)
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudent])
def enroll_course(request, subject_id):
    """Enroll student in a course"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        subject = Subject.objects.get(id=subject_id, is_active=True)
    except Subject.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already enrolled
    if student.subjects.filter(id=subject_id).exists():
        return Response({
            'message': 'Already enrolled in this course',
            'course': SubjectSerializer(subject).data
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Enroll the student
    student.subjects.add(subject)
    
    return Response({
        'message': 'Successfully enrolled in course',
        'course': SubjectSerializer(subject).data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsProfessor])
def professor_courses(request):
    """Get all available courses for professor - shows enrolled status"""
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        return Response({'error': 'Professor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get all active subjects
    all_subjects = Subject.objects.filter(is_active=True)
    
    # Get enrolled subject IDs (subjects professor teaches)
    enrolled_subject_ids = set(professor.subjects.filter(is_active=True).values_list('id', flat=True))
    
    # Serialize subjects with enrollment status
    courses_data = []
    for subject in all_subjects:
        subject_data = SubjectSerializer(subject).data
        subject_data['is_enrolled'] = subject.id in enrolled_subject_ids
        courses_data.append(subject_data)
    
    return Response({
        'courses': courses_data,
        'total_courses': len(courses_data),
        'enrolled_count': len(enrolled_subject_ids)
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsProfessor])
def enroll_professor_course(request, subject_id):
    """Enroll professor in a course (assign subject to professor)"""
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        return Response({'error': 'Professor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        subject = Subject.objects.get(id=subject_id, is_active=True)
    except Subject.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already enrolled (already teaching this subject)
    if professor.subjects.filter(id=subject_id).exists():
        return Response({
            'message': 'Already teaching this course',
            'course': SubjectSerializer(subject).data
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Enroll the professor (assign subject)
    professor.subjects.add(subject)
    
    return Response({
        'message': 'Successfully enrolled in course',
        'course': SubjectSerializer(subject).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsProfessor])
def enroll_student(request, student_id, subject_id):
    """Enroll a student in a course that the professor teaches"""
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        return Response({'error': 'Professor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        student = Student.objects.get(id=student_id, is_active=True)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        subject = Subject.objects.get(id=subject_id, is_active=True)
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Verify professor teaches this subject
    if subject not in professor.subjects.all():
        return Response({'error': 'You do not teach this subject'}, status=status.HTTP_403_FORBIDDEN)
    
    # Check if already enrolled
    if student.subjects.filter(id=subject_id).exists():
        return Response({
            'message': 'Student is already enrolled in this course',
            'course': SubjectSerializer(subject).data
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Enroll the student
    student.subjects.add(subject)
    
    return Response({
        'message': 'Student successfully enrolled in course',
        'course': SubjectSerializer(subject).data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsProfessor])
def get_student_grades(request, student_id, subject_id=None):
    """Get grades for a student in professor's subjects"""
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        return Response({'error': 'Professor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        student = Student.objects.get(id=student_id, is_active=True)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get professor's subjects
    professor_subjects = professor.subjects.all()
    
    # Check if student is enrolled in any of professor's subjects
    student_subjects = student.subjects.filter(id__in=professor_subjects.values_list('id', flat=True))
    
    if not student_subjects.exists():
        return Response({'error': 'Student is not enrolled in any of your subjects'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get grades
    if subject_id:
        # Get grade for specific subject
        try:
            subject = Subject.objects.get(id=subject_id)
            if subject not in professor_subjects:
                return Response({'error': 'You do not teach this subject'}, status=status.HTTP_403_FORBIDDEN)
            
            grades = Grade.objects.filter(student=student, subject=subject, professor=professor)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # Get all grades for student in professor's subjects
        grades = Grade.objects.filter(student=student, subject__in=professor_subjects, professor=professor)
    
    serializer = GradeSerializer(grades, many=True)
    return Response({
        'student': StudentSerializer(student).data,
        'grades': serializer.data
    })


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated, IsProfessor])
def grade_student(request, student_id, subject_id):
    """Create or update a grade for a student in a subject"""
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        return Response({'error': 'Professor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        student = Student.objects.get(id=student_id, is_active=True)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        subject = Subject.objects.get(id=subject_id, is_active=True)
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Verify professor teaches this subject
    if subject not in professor.subjects.all():
        return Response({'error': 'You do not teach this subject'}, status=status.HTTP_403_FORBIDDEN)
    
    # Verify student is enrolled in this subject
    if subject not in student.subjects.all():
        return Response({'error': 'Student is not enrolled in this subject'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create grade
    grade, created = Grade.objects.get_or_create(
        student=student,
        subject=subject,
        professor=professor,
        defaults={'grade': request.data.get('grade'), 'notes': request.data.get('notes', '')}
    )
    
    if not created:
        # Update existing grade
        grade.grade = request.data.get('grade', grade.grade)
        grade.notes = request.data.get('notes', grade.notes)
        grade.save()
    
    serializer = GradeSerializer(grade)
    return Response({
        'message': 'Grade saved successfully',
        'grade': serializer.data
    }, status=status.HTTP_200_OK)


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
