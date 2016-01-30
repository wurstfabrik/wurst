from rest_framework import serializers


def serializer_factory(model, serializer_class=serializers.ModelSerializer, attrs=None, meta=None):
    """
    Generate a simple serializer for the given model class.

    :param model: Model class
    :param serializer_class: Serializer base class
    :param attrs: Serializer class attrs
    :param meta: Serializer Meta class attrs
    :return: a Serializer class
    """
    attrs = attrs or {}
    meta = meta or {}
    meta.setdefault("model", model)
    attrs.setdefault("Meta", type(str("Meta"), (object,), meta))
    return type(str("%sSerializer" % model.__name__), (serializer_class,), attrs)
