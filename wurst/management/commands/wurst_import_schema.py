import toml
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from wurst.utils.schema_import import SchemaImporter


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file")

    @atomic
    def handle(self, file, **options):
        with open(file, "r") as infp:
            data = toml.load(infp)

        schitter = SchemaImporter()
        schitter.stderr = self.stderr
        schitter.import_from_data(data)

