# -- encoding: UTF-8 --
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist, ValidationError
from django.utils.encoding import force_text
from rest_framework.fields import Field
from rest_framework.relations import RelatedField

USUAL_KEY_FIELDS = ("pk", "slug")


def unserialize_by_scalar(queryset, value, key_fields=USUAL_KEY_FIELDS):
    for field in key_fields:
        try:
            return queryset.get(**{field: value})
        except (ObjectDoesNotExist, TypeError, ValueError):
            pass
    raise ValidationError("No object matches %r" % value)


class ScalarUnserializerMixin:
    scalar_key_fields = USUAL_KEY_FIELDS
    def to_internal_value(self, data):
        if not isinstance(data, (dict, list)):
            if hasattr(self, "get_queryset"):  # used on RelatedFields?
                queryset = self.get_queryset()
            elif hasattr(self, "Meta"):  # used on Serializers?
                queryset = self.Meta.model.objects.all()
            else:
                raise ImproperlyConfigured("ScalarUnserializerMixin used on %r, unsupported" % self)
            return unserialize_by_scalar(queryset, data, key_fields=self.scalar_key_fields)
        return super(ScalarUnserializerMixin, self).to_internal_value(self, data)


class SlugOrPKRelatedField(ScalarUnserializerMixin, RelatedField):
    def __init__(self, slug_field="slug", **kwargs):
        self.slug_field = slug_field
        RelatedField.__init__(self, **kwargs)

    def to_internal_value(self, data):
        return unserialize_by_scalar(self.get_queryset(), data)

    def use_pk_only_optimization(self):
        return False

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


class EnumField(Field):
    """
    A field for enums (of Py3 or enumfields sort).
    """

    def __init__(self, enum_cls=None, **kwargs):
        super(EnumField, self).__init__(**kwargs)
        self.enum_cls = enum_cls

    def to_internal_value(self, data):
        try:
            return self.enum_cls(data)
        except (TypeError, ValueError):
            data = force_text(data).lower()
            for key, value in self.enum_cls.__members__.items():
                if key.lower() == data:
                    return value

    def to_representation(self, obj):
        assert isinstance(obj, self.enum_cls)
        return obj.name.lower()
