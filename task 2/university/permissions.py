from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Only admin users can access."""
    def has_permission(self, request, view):
        return hasattr(request.user, 'administrator')


class IsProfessor(BasePermission):
    """Only professor users can access."""
    def has_permission(self, request, view):
        return hasattr(request.user, 'professor')


class IsStudent(BasePermission):
    """Only student users can access."""
    def has_permission(self, request, view):
        return hasattr(request.user, 'student')


class IsAdminOrProfessor(BasePermission):
    """Admin or professor can access."""
    def has_permission(self, request, view):
        return hasattr(request.user, 'administrator') or hasattr(request.user, 'professor')
