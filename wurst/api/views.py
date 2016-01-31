from rest_framework import permissions, serializers, viewsets
from wurst.api.fields import SlugOrPKRelatedField

from wurst.api.utils import serializer_factory
from wurst.models import Issue, Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = serializer_factory(Project)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)



class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
    serializer_related_field = SlugOrPKRelatedField

    def get_fields(self):
        fields = super(IssueSerializer, self).get_fields()
        for field in ("status", "key", "priority"):  # These can be inferred in `save`
            fields[field].required = False
        return fields


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
