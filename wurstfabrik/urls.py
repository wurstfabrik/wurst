from django.conf.urls import include, url
from django.contrib import admin

from wurst.api.router import get_router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(get_router().urls, namespace='v1')),

]
