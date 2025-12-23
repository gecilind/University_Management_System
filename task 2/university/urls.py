from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'faculties', views.FacultyViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'administrators', views.AdministratorViewSet)
router.register(r'professors', views.ProfessorViewSet)
router.register(r'students', views.StudentViewSet)

app_name = 'university'

urlpatterns = [
    path('', include(router.urls)),
    path('users/', views.get_users, name='get_users'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('renew/', views.renew_token_view, name='renew'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('professor-dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('courses/', views.student_courses, name='student_courses'),
    path('professor-courses/', views.professor_courses, name='professor_courses'),
    path('enroll/<int:subject_id>/', views.enroll_course, name='enroll_course'),
    path('enroll-professor/<int:subject_id>/', views.enroll_professor_course, name='enroll_professor_course'),
    path('enroll-student/<int:student_id>/<int:subject_id>/', views.enroll_student, name='enroll_student'),
    path('grade/<int:student_id>/<int:subject_id>/', views.grade_student, name='grade_student'),
    path('grades/<int:student_id>/', views.get_student_grades, name='get_student_grades'),
    path('grades/<int:student_id>/<int:subject_id>/', views.get_student_grades, name='get_student_grade'),
]
