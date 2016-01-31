# -- encoding: UTF-8 --
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management.commands.migrate import Command as MigCommand
from django.db.utils import DEFAULT_DB_ALIAS

from wurst.models import Project

from .wurst_import_schema import Command as WISCommand


class Command(BaseCommand):
    """
    Seed the application with models suitable for development.
    """

    def handle(self, *args, **options):
        MigCommand().handle(database=DEFAULT_DB_ALIAS, app_label=(), **options)
        schema_path = os.path.join(
            os.path.dirname(__file__),
            "..",  # management
            "..",  # wurst
            "schemata",
            "basic.toml"
        )
        WISCommand().handle(file=schema_path, **options)
        user_model = get_user_model()
        if not user_model.objects.filter(is_superuser=True).exists():
            user_model.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write("Created superuser (username = admin, password = admin)")
        if not Project.objects.exists():
            Project.objects.create(slug="test", name="Test", prefix="T-")
            self.stdout.write("Created Test project")
