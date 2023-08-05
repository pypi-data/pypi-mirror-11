from controller.conf.base_settings import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

TEMPLATE_DEBUG = True

CELERY_SEND_TASK_ERROR_EMAILS = False


# When DEBUG is enabled Django appends every executed SQL statement to django.db.connection.queries
# this will grow unbounded in a long running process environment like celeryd
if "celeryd" in sys.argv or 'celeryev' in sys.argv or 'celerybeat' in sys.argv:
    DEBUG = False
