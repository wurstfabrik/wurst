from rest_framework import permissions, viewsets

from wurst.api.utils import serializer_factory
from wurst.models import Issue, Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = serializer_factory(Project)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = serializer_factory(Project)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
