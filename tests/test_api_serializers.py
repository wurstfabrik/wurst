# -- encoding: UTF-8 --
import json

import pytest
from rest_framework.serializers import ModelSerializer
from wurst.api.serializers import StatusSerializer, ProjectSerializer
from wurst.core.models import Status, Issue


def test_status_serialization():
    json.dumps(StatusSerializer().to_representation(Status()))  # This would raise at misserialization of the enum


@pytest.mark.django_db
def test_scalar_unserializer(project):
    assert ProjectSerializer().to_internal_value(project.pk) == project
    assert ProjectSerializer().to_internal_value(project.slug) == project


@pytest.mark.django_db
def test_scalar_unserializer_as_field(project):
    class MockIssueSerializer(ModelSerializer):
        class Meta:
            model = Issue
            fields = ("project",)

        project = ProjectSerializer()

    assert MockIssueSerializer().to_internal_value({"project": project.pk})["project"] == project
