import os

# HACK: Only needed for testing!
os.environ.setdefault('_SENTRY_SKIP_CONFIGURATION', '1')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentry.conf.server')
