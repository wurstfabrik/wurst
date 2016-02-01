# -- encoding: UTF-8 --
from rest_framework import serializers

from wurst.api.fields import (
    EnumField, ScalarUnserializerMixin, SlugOrPKRelatedField
)
from wurst.core.consts import StatusCategory
from wurst.core.models import Issue, IssueType, Priority, Project, Status


class StatusSerializer(ScalarUnserializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Status
    category = EnumField(enum_cls=StatusCategory)


class IssueTypeSerializer(ScalarUnserializerMixin, serializers.ModelSerializer):
    class Meta:
        model = IssueType


class PrioritySerializer(ScalarUnserializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Priority


class ProjectSerializer(ScalarUnserializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Project


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue

    serializer_related_field = SlugOrPKRelatedField
    project = ProjectSerializer()
    status = StatusSerializer()
    type = IssueTypeSerializer()
    priority = PrioritySerializer()

    def get_fields(self):
        fields = super(IssueSerializer, self).get_fields()
        for field in ("status", "key", "priority"):  # These can be inferred in `save`
            fields[field].required = False
        return fields
