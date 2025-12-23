from django.db import models
from django.contrib.auth.models import User

# Base class for common fields (DRY principle)
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# Faculty Model
class Faculty(BaseModel):
    DEPARTMENTS = (
        ('CS', 'Computer Science'),
        ('EN', 'English'),
    )
    
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_department_display()}"
    
    class Meta:
        verbose_name_plural = "Faculties"


# Subject Model
class Subject(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='subjects')
    credits = models.IntegerField(default=3)
    
    def __str__(self):
        return f"{self.code} - {self.name}"


# Administrator Model
class Administrator(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrator')
    phone = models.CharField(max_length=15, blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Admin - {self.user.get_full_name() or self.user.username}"


# Professor Model
class Professor(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='professors')
    specialization = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    office_hours = models.CharField(max_length=100, blank=True)
    subjects = models.ManyToManyField(Subject, related_name='professors', blank=True)
    
    def __str__(self):
        return f"Prof. {self.user.get_full_name() or self.user.username}"


# Student Model
class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    enrollment_number = models.CharField(max_length=20, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='students')
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    subjects = models.ManyToManyField(Subject, related_name='students', blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.enrollment_number}"


# Grade Model - for storing student grades per subject
class Grade(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='given_grades')
    grade = models.DecimalField(max_digits=5, decimal_places=2, help_text='Grade value (0-100)')
    notes = models.TextField(blank=True, help_text='Optional notes about the grade')
    
    class Meta:
        unique_together = ['student', 'subject', 'professor']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.subject.code}: {self.grade}"


# Refresh Token Model
class RefreshToken(models.Model):
    token = models.CharField(max_length=256, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"RefreshToken for {self.user.username} (expires: {self.expires_at})"
    
    class Meta:
        db_table = 'university_refreshtoken'
