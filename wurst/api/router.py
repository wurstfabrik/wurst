from rest_framework.routers import DefaultRouter

from wurst.api.views import IssueViewSet, ProjectViewSet


def get_router():
    router = DefaultRouter()
    router.register(r'projects', ProjectViewSet)
    router.register(r'issues', IssueViewSet)
    return router
