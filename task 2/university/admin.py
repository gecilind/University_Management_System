from django.contrib import admin
from .models import Faculty, Subject, Administrator, Professor, Student, RefreshToken


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'is_active', 'created_at')
    list_filter = ('department', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'faculty', 'credits', 'is_active')
    list_filter = ('faculty', 'is_active')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'office_location', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'specialization', 'phone', 'is_active')
    list_filter = ('faculty', 'is_active')
    search_fields = ('user__username', 'user__email', 'specialization')
    filter_horizontal = ('subjects',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment_number', 'faculty', 'gpa', 'is_active')
    list_filter = ('faculty', 'is_active')
    search_fields = ('user__username', 'user__email', 'enrollment_number')
    filter_horizontal = ('subjects',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'expires_at', 'created_at')
    list_filter = ('expires_at', 'created_at')
    search_fields = ('user__username', 'token')
    readonly_fields = ('token', 'created_at')
