from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Faculty, Subject, Administrator, Professor, Student, Grade


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'name', 'department', 'description', 'is_active')


class SubjectSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'code', 'description', 'faculty', 'faculty_name', 'credits', 'is_active')


class AdministratorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administrator
        fields = ('id', 'user', 'phone', 'office_location', 'is_active')


class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Professor
        fields = ('id', 'user', 'faculty', 'faculty_name', 'specialization', 'phone', 'office_hours', 'subjects', 'is_active')


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'user', 'enrollment_number', 'faculty', 'faculty_name', 'date_of_birth', 'phone', 'subjects', 'gpa', 'is_active')


class DashboardAdminSerializer(serializers.Serializer):
    """Serializer for admin dashboard data"""
    total_students = serializers.IntegerField()
    total_professors = serializers.IntegerField()
    total_subjects = serializers.IntegerField()
    total_faculties = serializers.IntegerField()
    recent_enrollments = StudentSerializer(many=True)


class DashboardProfessorSerializer(serializers.Serializer):
    """Serializer for professor dashboard data"""
    professor = ProfessorSerializer()
    subjects = SubjectSerializer(many=True)
    students = StudentSerializer(many=True)
    students_count = serializers.IntegerField()


class DashboardStudentSerializer(serializers.Serializer):
    """Serializer for student dashboard data"""
    student = StudentSerializer()
    enrolled_subjects = SubjectSerializer(many=True)
    gpa = serializers.DecimalField(max_digits=3, decimal_places=2)


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    student_enrollment = serializers.CharField(source='student.enrollment_number', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    professor_name = serializers.CharField(source='professor.user.get_full_name', read_only=True)

    class Meta:
        model = Grade
        fields = ('id', 'student', 'student_name', 'student_username', 'student_enrollment',
                  'subject', 'subject_code', 'subject_name', 'professor', 'professor_name',
                  'grade', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
