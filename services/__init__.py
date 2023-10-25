import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'replicator.settings'
django.setup()
