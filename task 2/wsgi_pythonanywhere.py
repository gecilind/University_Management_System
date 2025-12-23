# WSGI Configuration for PythonAnywhere

import os
import sys

# Add your project directory to the sys.path
project_home = os.path.expanduser('~/mysite')
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Configure Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'university_project.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
