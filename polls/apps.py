"""App basic settings."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Setting a default of AppConfig."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
