from rest_framework import serializers


def serializer_factory(model, serializer_class=serializers.ModelSerializer, attrs=None, meta=None):
    attrs = attrs or {}
    meta = meta or {}
    meta.setdefault("model", model)
    attrs.setdefault("Meta", type(str("Meta"), (object,), meta))
    return type(str("%sSerializer" % model.__name__), (serializer_class,), attrs)
