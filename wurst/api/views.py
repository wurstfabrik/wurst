from django.db import transaction
from rest_framework import permissions, viewsets
from reversion import revisions as reversion

from wurst.api.serializers import CommentSerializer, IssueSerializer, ProjectSerializer
from wurst.core.models import Comment, Issue, Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def perform_create(self, serializer):
        with transaction.atomic(), reversion.create_revision():
            serializer.save(creator=self.request.user)
            reversion.set_user(self.request.user)

    def perform_update(self, serializer):
        with transaction.atomic(), reversion.create_revision():
            serializer.save()
            reversion.set_user(self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    # TODO: Would be nice to use `drf-nested-routers` for a nicer API
    # TODO: Prevent users modifying each others' comments
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def perform_create(self, serializer):
        with transaction.atomic(), reversion.create_revision():
            serializer.save(creator=self.request.user)
            reversion.set_user(self.request.user)

    def perform_update(self, serializer):
        with transaction.atomic(), reversion.create_revision():
            serializer.save()
            reversion.set_user(self.request.user)
