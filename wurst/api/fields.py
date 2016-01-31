# -- encoding: UTF-8 --
import six
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField


class SlugOrPKRelatedField(SlugRelatedField, PrimaryKeyRelatedField):
    def use_pk_only_optimization(self):
        return False

    def __init__(self, slug_field="slug", **kwargs):
        super(SlugOrPKRelatedField, self).__init__(slug_field=slug_field, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, six.integer_types):  # Smells like a PK
            return PrimaryKeyRelatedField.to_internal_value(self, data)
        return SlugRelatedField.to_internal_value(self, data)

    def to_representation(self, obj):
        if not (obj and obj.pk):
            return None

        slug = getattr(obj, self.slug_field, None)
        val = {
            "id": obj.pk,
        }
        if slug:
            val[self.slug_field] = slug
        return val
