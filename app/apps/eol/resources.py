
from import_export import resources
from apps.eol.models import Vendor, Product, Software

class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendor
        fields = (
            "id",
            "name",
        )
        export_order = ("id", "name")


class EntityResource(resources.ModelResource):
    class Meta:
        fields = (
            "id",
            "vendor__name",
            "name",
            "end_of_life_announced_date",
            "end_of_engineering_date",
            "end_of_sale_date",
            "end_of_life_date",
            "created_at",
            "updated_at",
        )
        export_order = (
            "id",
            "vendor__name",
            "name",
            "end_of_life_announced_date",
            "end_of_engineering_date",
            "end_of_sale_date",
            "end_of_life_date",
            "created_at",
            "updated_at",
        )

class ProductResource(EntityResource):
    class Meta(EntityResource.Meta):
        model = Product

class SoftwareResource(resources.ModelResource):
    class Meta(EntityResource.Meta):
        model = Software
