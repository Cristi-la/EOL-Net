from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include("apps.eol.urls")),
    path('api/v1/', include("apps.api.urls")),
    path('api/latest/', include("apps.api.urls")),
]
