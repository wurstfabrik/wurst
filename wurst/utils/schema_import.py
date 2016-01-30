import sys
from collections import defaultdict

from wurst.models import IssueType, Priority, Status


class SchemaImporter:
    stderr = sys.stderr
    type_to_class = {
        "type": IssueType,
        "status": Status,
        "priority": Priority
    }

    def __init__(self):
        self.objects = defaultdict(dict)

    def import_from_data(self, data):
        for type, items in data.items():
            if not isinstance(items, list):
                continue
            importer = getattr(self, "import_%s" % type, None)
            if not importer:
                if type in self.type_to_class:
                    importer = self.generic_importer
            if not importer:
                self.stderr.write("No importer for %r" % type)
            for val in items:
                importer(type, val)

    def generic_importer(self, type, datum):
        model_class = self.type_to_class[type]
        obj = model_class.objects.create(**datum)
        self.objects[type][obj.slug] = obj
