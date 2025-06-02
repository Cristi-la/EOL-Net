# apps/eol/admin.py

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.db.models import Count

from apps.eol.models import Vendor, Product, Software
from apps.eol.resources import VendorResource, ProductResource, SoftwareResource


@admin.register(Vendor)
class VendorAdmin(ImportExportModelAdmin):
    resource_class = VendorResource

    list_display = ("name", "product_count", "software_count")
    search_fields = ("name",)
    ordering = ("name",)
    list_filter = ("name",)

    def product_count(self, obj):
        return obj._product_count
    product_count.short_description = "Products"

    def software_count(self, obj):
        return obj._software_count
    software_count.short_description = "Software Packages"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _product_count=Count("products", distinct=True),
            _software_count=Count("software_packages", distinct=True),
        )


class EntityAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = (
        "name",
        "vendor",
        "end_of_life_announced_date",
        "end_of_life_date",
    )
    search_fields = (
        "name",
        "vendor__name",
    )
    list_filter = (
        "vendor",
        "end_of_life_date",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_select_related = ("vendor",)
    fieldsets = (
        (None, {
            "fields": (
                "name",
                "vendor",
            )
        }),
        ("Lifecycle Dates", {
            "fields": (
                "end_of_life_announced_date",
                "end_of_engineering_date",
                "end_of_sale_date",
                "end_of_life_date",
            )
        }),
        ("Timestamps", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


class SoftwareAdmin(EntityAdmin):
    resource_class = SoftwareResource

class ProductAdmin(EntityAdmin):
    resource_class = ProductResource

admin.site.register(Product, ProductAdmin)
admin.site.register(Software, SoftwareAdmin)