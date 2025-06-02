from django.db import models

class LifecycleMixin(models.Model):
    """
    Abstract base class to hold common lifecycle (EOL/EOS) fields for any product.
    """

    # — Announcement when EOL/EOS was first publicly declared
    end_of_life_announced_date = models.DateField(
        blank=True, null=True,
        help_text="Date the product's End-of-Life was announced."
    )

    # — Date when the product was officially declared EOL/EOS
    end_of_life_date = models.DateField(
        blank=True, null=True,
        help_text="Final date of support (End-of-Life)."
    )

    # — Date when the product was officially declared End-of-Sale
    end_of_engineering_date = models.DateField(
        blank=True, null=True,
        help_text="Date when the software package was officially declared End-of-Engineering."
    )

    # — Date when the product was officially declared End-of-Sale
    end_of_sale_date = models.DateField(
        blank=True, null=True,
        help_text="Date when the product was officially declared End-of-Sale."
    )

    class Meta:
        abstract = True


class TimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractEntity(
    LifecycleMixin,
    TimeMixin,
    models.Model,
):
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} ({self.vendor.name})"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, vendor={self.vendor.name})"
    
