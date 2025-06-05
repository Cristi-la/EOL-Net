# apps/eol/serializers.py

from rest_framework import serializers
from apps.eol.models import Vendor, Product, Software



#
# ─── 1) VENDOR SERIALIZER ───────────────────────────────────────────────────────────
#
class VendorSerializer(serializers.ModelSerializer):
    """
    Serializer for Vendor model.
    """
    class Meta:
        model = Vendor
        fields = [
            "id",
            "name",
        ]
        read_only_fields = ["id"]


#
# ─── 2) BASE ENTITY SERIALIZER (for Product & Software) ────────────────────────────
#
class EntitySerializer(serializers.ModelSerializer):
    """
    Base serializer that defines shared fields for models inheriting AbstractEntity.
    Subclasses must set `Meta.model` to their target model.
    """
    vendor_name = serializers.CharField(
        source="vendor.name",
        read_only=True,
        help_text="Vendor name (read-only)"
    )
    vendor = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(),
        help_text="ID of the Vendor"
    )

    class Meta:
        model = None  # will be overridden in subclasses
        fields = [
            "id",
            "vendor",               # writeable FK to Vendor
            "vendor_name",          # read-only vendor name
            "name",
            "end_of_life_announced_date",
            "end_of_engineering_date",
            "end_of_sale_date",
            "end_of_life_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "vendor_name",
            "created_at",
            "updated_at",
        ]

#
# ─── 3) PRODUCT SERIALIZER ──────────────────────────────────────────────────────────
#
class ProductSerializer(EntitySerializer):
    class Meta(EntitySerializer.Meta):
        model = Product


#
# ─── 4) SOFTWARE SERIALIZER ─────────────────────────────────────────────────────────
#
class SoftwareSerializer(EntitySerializer):
    class Meta(EntitySerializer.Meta):
        model = Software
