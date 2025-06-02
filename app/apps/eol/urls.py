from django.urls import path
from apps.eol.views import index


urlpatterns = [
    path('', index, name='eol_index'),
]