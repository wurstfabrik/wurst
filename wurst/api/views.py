from rest_framework import permissions, viewsets

from wurst.api.serializers import IssueSerializer, ProjectSerializer
from wurst.core.models import Issue, Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
