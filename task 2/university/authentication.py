from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from django.contrib.auth.models import User
import jwt
from django.conf import settings


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication that reads token from Authorization header.
    Format: Authorization: Bearer <token>
    """
    
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'Bearer'
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        # If no Authorization header, check if this is an AllowAny endpoint
        if not auth_header:
            # List of endpoints that allow anonymous access
            allow_any_paths = ['/api/login/', '/api/logout/', '/api/renew/']
            path = request.path
            
            # If it's an AllowAny endpoint, return None (let permission class handle it)
            # This allows AllowAny endpoints to work without authentication
            if any(path.endswith(allowed_path) for allowed_path in allow_any_paths):
                return None
            
            # For protected endpoints without token, raise NotAuthenticated (401)
            # This ensures we get 401 instead of 403 from permission classes.
            # By raising NotAuthenticated here, we prevent SessionAuthentication
            # from setting request.user to AnonymousUser, which would cause
            # permission classes to raise PermissionDenied (403) instead.
            raise NotAuthenticated('Authentication credentials were not provided')
        
        # Check if header starts with 'Bearer '
        if not auth_header.startswith('Bearer '):
            # Invalid format - raise AuthenticationFailed to get 401
            raise AuthenticationFailed('Invalid authorization header format')
        
        # Extract token
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed('Invalid authorization header format')
        
        try:
            # Decode and verify token
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            # Get user from payload
            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed('Invalid token payload')
            
            try:
                user = User.objects.get(id=user_id, is_active=True)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found or inactive')
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            # Token expired - raise AuthenticationFailed to get 401 (so interceptor can renew)
            raise AuthenticationFailed('Token has expired')
        except (jwt.DecodeError, jwt.InvalidTokenError):
            # Invalid token - raise AuthenticationFailed to get 401 (so interceptor can renew)
            raise AuthenticationFailed('Invalid token')
        except AuthenticationFailed:
            # Re-raise AuthenticationFailed exceptions
            raise
        except Exception as e:
            # Any other error - raise AuthenticationFailed
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')

