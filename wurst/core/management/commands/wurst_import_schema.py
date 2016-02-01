from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from wurst.core.utils.schema_import import SchemaImporter


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file")

    @atomic
    def handle(self, file, **options):
        schitter = SchemaImporter()
        schitter.stdout = self.stdout
        schitter.stderr = self.stderr

        with open(file, "r") as infp:
            schitter.import_from_toml(infp)
