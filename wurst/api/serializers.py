# -- encoding: UTF-8 --
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import empty

from wurst.api.fields import EnumField, ScalarUnserializerMixin, SlugOrPKRelatedField
from wurst.core.consts import StatusCategory
from wurst.core.models import Comment, Issue, IssueType, Priority, Project, Status


class UserSerializer(ScalarUnserializerMixin, serializers.ModelSerializer):
    scalar_key_fields = ("pk", "username")

    class Meta:
        model = get_user_model()


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
    status = StatusSerializer(required=False)
    type = IssueTypeSerializer()
    priority = PrioritySerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    creator = UserSerializer(read_only=True)

    def get_fields(self):
        fields = super(IssueSerializer, self).get_fields()
        fields["key"].required = False  # Inferred in `save`
        fields["key"].read_only = True
        return fields
