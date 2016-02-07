# -- encoding: UTF-8 --
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

    creator = UserSerializer(read_only=True)


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
    transition = serializers.CharField(required=False, write_only=True)

    def get_fields(self):
        fields = super(IssueSerializer, self).get_fields()
        fields["key"].required = False  # Inferred in `save`
        fields["key"].read_only = True
        if self.many:  # List context? No comments, please.
            fields.pop("comments", None)
        return fields

    def __init__(self, instance=None, data=empty, **kwargs):
        self.many = bool(kwargs.get("many"))
        super(IssueSerializer, self).__init__(instance, data, **kwargs)

    def validate_status(self, value):
        if self.instance and self.instance.has_transitions():
            raise ValidationError("May not directly set the status of an issue whose type has transitions")
        return value

    def update(self, instance, validated_data):
        transition = validated_data.pop("transition", None)
        instance = super(IssueSerializer, self).update(instance, validated_data)
        if transition:
            instance.transition(transition)
            instance.save()
        return instance
