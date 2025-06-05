from django.db import models
from django.contrib.auth import get_user_model
from apps.eol.models import Vendor
from apps.eol.abstracts import TimeMixin
from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta
from django.utils import timezone
import binascii
import os

from django.core.exceptions import ValidationError

User = get_user_model()

class APIToken(
    TimeMixin,
): 
    THROTTLE_CHOICES = [
        ("anon", "Anonymous Rate"),
        ("default", "Default Rate"),
        ("ha", "High Availability Rate"),
    ]


    name = models.CharField(max_length=200, unique=True, help_text="A human-friendly name")
    key = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
        help_text="Unguessable random string used as token identifier"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_tokens",
        help_text="User who “owns” this token"
    )

    can_write = models.BooleanField(
        default=False,
        help_text="Allow creating (POST) objects for selected vendors."
)
    can_edit = models.BooleanField(
        default=False,
        help_text="Allow editing (PUT/PATCH) existing objects for selected vendors."
    )
    can_delete = models.BooleanField(
        default=False,
        help_text="Allow deleting (DELETE) existing objects for selected vendors."
    )
    
    allowed_vendors = models.ManyToManyField(
        Vendor,
        blank=True,
        help_text="List of Vendor IDs this token is allowed to write to (if can_write=True)."
    )

    throttle_scope = models.CharField(
        max_length=10,
        choices=THROTTLE_CHOICES,
        default="default",
        help_text="Pick which rate limit this token should use."
    )

    valid_until = models.DateTimeField(
        help_text="Date/time when this token becomes invalid.",
        default=timezone.now() + timedelta(days=365),
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        super().save(*args, **kwargs)

    def clean(self):
        if self.valid_until <= timezone.now():
            raise ValidationError({"valid_until": "The valid_until date must be in the future."})

        return super().clean()

    def generate_jwt(self):
        """
        Produce a JWT that carries:
          - token_key (so we can lookup the row if needed for revocation)
          - can_write (bool)
          - allowed_vendors (list of vendor IDs)
          - valid_until (timestamp)
        The AccessToken expiration is set to `self.valid_until`.
        """
        token = AccessToken()
        lifetime = self.valid_until - timezone.now()
        token.set_exp(from_time=timezone.now(), lifetime=lifetime)

        token["token_key"]       = self.key
        token["can_write"] = self.can_write
        token["can_edit"] = self.can_edit
        token["can_delete"] = self.can_delete
        token["valid_until"]     = int(self.valid_until.timestamp())
        
        token["throttle_scope"] = self.throttle_scope
        token["valid_until"] = int(self.valid_until.timestamp())
        token["user_id"] = self.user_id

        return str(token)

    @property
    def is_valid(self):
        return timezone.now() < self.valid_until
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "API Token"
        verbose_name_plural = "API Tokens"