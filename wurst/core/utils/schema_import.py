import sys
from collections import defaultdict

import toml

from wurst.core.models import IssueType, Priority, Status


class SchemaImporter:
    """
    An utility to import an issue type/priority/status/... schema.

    After the import is finished, the ``objects`` field will be populated
    with the imported objects.
    """

    stderr = sys.stderr
    stdout = sys.stdout

    type_to_class = {
        "type": IssueType,
        "status": Status,
        "priority": Priority
    }

    def __init__(self):
        self.objects = defaultdict(dict)

    def import_from_toml(self, fp):
        """
        Import from a file-like object where TOML markup can be read from.

        :param fp: A filelike object.
        :return: Naught.
        """
        data = toml.load(fp)
        self.import_from_data(data)

    def import_from_data(self, data):
        """
        Import objects into the database from the given data dictionary.

        :param data: Data dictionary
        :type data: dict[str,list[dict]]
        :return: Does not return a value, but the instance's
                 `.objects` dict will have been modified
        """
        for obj_type, items in data.items():
            if not isinstance(items, list):
                continue
            importer = getattr(self, "import_%s" % obj_type, None)
            if not importer:
                if obj_type in self.type_to_class:
                    importer = self.generic_importer
            if not importer:
                self.stderr.write("No importer for %r" % obj_type)
            for val in items:
                importer(obj_type, val)

    def generic_importer(self, obj_type, datum):
        """
        Import an object using the `type_to_class` mapping.

        As an added bonus, will not try reimporting objects if a slug
        is specified.

        :param obj_type: Object type string, e.g. "priority"
        :param datum: An object datum
        :type datum: dict[str,object]
        :return: The created object.
        """
        model_class = self.type_to_class[obj_type]
        obj = None
        if "slug" in datum:  # See if we already got one...
            obj = model_class.objects.filter(slug=datum["slug"]).first()
        if obj is None:  # Not found? Create it.
            obj = model_class.objects.create(**datum)
        idfr = getattr(obj, "slug", obj.pk)
        self.objects[obj_type][idfr] = obj
        self.stdout.write("%s processed: %s" % (obj_type.title(), idfr))
        return obj
