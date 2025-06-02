from django.db import models
from apps.eol.abstracts import AbstractEntity

class Vendor(models.Model):
    name = models.CharField(
        max_length=300,
        unique=True,
        help_text="Vendor or manufacturer name."
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self):
        return self.name


class Product(AbstractEntity):
    name = models.CharField(
        max_length=300,
        help_text="Product name."
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="products",
        help_text="Vendor or manufacturer of the product."
    )

    class Meta:
        unique_together = [
            ("vendor", "name")
        ]
        indexes = [
            models.Index(fields=["vendor", "name"]),
        ]
        ordering = ["vendor__name", "name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    
class Software(AbstractEntity):
    name = models.CharField(
        max_length=300,
        help_text="OS/Software/firmware name."
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="software_packages",
        help_text="Vendor or manufacturer of the software package."
    )

    class Meta:
        unique_together = [
            ("vendor", "name")
        ]
        indexes = [
            models.Index(fields=["vendor", "name"]),
        ]
        ordering = ["vendor__name", "name"]
        verbose_name = "Software Package"
        verbose_name_plural = "Software Packages"
