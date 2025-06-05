from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path, include
from apps.api.views import VendorViewSet, ProductViewSet, SoftwareViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"vendors", VendorViewSet, basename="vendor")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"software", SoftwareViewSet, basename="software")

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path("", include(router.urls)),
]