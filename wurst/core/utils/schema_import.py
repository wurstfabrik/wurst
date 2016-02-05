import sys
from collections import defaultdict, OrderedDict

import toml

from wurst.core.models import IssueType, Priority, Status, Transition


def sift(iterable, predicate):
    """
    Sift an iterable into two lists, those which pass the predicate and those who don't.

    :param iterable:
    :param predicate:
    :return: (True-list, False-list)
    :rtype: tuple[list, list]
    """
    t_list = []
    f_list = []
    for obj in iterable:
        (t_list if predicate(obj) else f_list).append(obj)
    return (t_list, f_list)


class SchemaImporter:
    """
    An utility to import an issue type/priority/status/... schema.

    After the import is finished, the ``objects`` field will be populated
    with the imported objects.
    """

    stderr = sys.stderr
    stdout = sys.stdout

    type_to_class = OrderedDict([
        ("type", IssueType),
        ("status", Status),
        ("priority", Priority),
        ("transition", Transition),
    ])

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
        for obj_type, klass in self.type_to_class.items():
            items = data.get(obj_type, [])
            if not isinstance(items, list):
                continue
            importer = getattr(self, "import_%s" % obj_type, None)
            if not importer:
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
        if hasattr(model_class, "mangle_import_datum"):
            datum = model_class.mangle_import_datum(datum)
        obj = None
        if "slug" in datum:  # See if we already got one...
            obj = model_class.objects.filter(slug=datum["slug"]).first()
        if obj is None:  # Not found? Create it.
            m2m_fields, non_m2m_fields = sift(datum.items(), lambda item: isinstance(item[1], list))
            obj = model_class.objects.create(**dict(non_m2m_fields))
            for field, value in m2m_fields:
                setattr(obj, field, value)
        idfr = getattr(obj, "slug", obj.pk)
        self.objects[obj_type][idfr] = obj
        self.stdout.write("%s processed: %s" % (obj_type.title(), idfr))
        return obj
