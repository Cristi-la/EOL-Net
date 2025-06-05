from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from apps.eol.models import Vendor, Product, Software
from apps.api.serializers import VendorSerializer, ProductSerializer, SoftwareSerializer

class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["name"]
    ordering_fields = ["name", "id"]
    ordering = ["name"]


class EntityViewSet(viewsets.ModelViewSet):
    queryset = None  # This will be set in subclasses
    serializer_class = None  # This will be set in subclasses
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "vendor": ["exact"],
        "end_of_life_date": ["lte", "gte", 'isnull'],
        "end_of_sale_date": ["lte", "gte", 'isnull'],
        "end_of_engineering_date": ["lte", "gte", 'isnull'],
        "end_of_life_announced_date": ["lte", "gte", 'isnull'],
    }
    search_fields = ["name", "vendor__name"]
    ordering_fields = ["name", "vendor__name", "end_of_life_date", "end_of_sale_date", "end_of_engineering_date", "end_of_life_announced_date"]
    ordering = ["vendor__name", "name"]


    def get_queryset(self):
        return self.queryset.select_related("vendor").all()


class ProductViewSet(EntityViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SoftwareViewSet(EntityViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer