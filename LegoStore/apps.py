from django.apps import AppConfig
import threading
import os


class LegostoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LegoStore'
    
