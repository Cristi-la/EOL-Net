# apps/api/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.api.models import APIToken


class APITokenForm(forms.ModelForm):
    class Meta:
        model = APIToken
        fields = [
            "name",
            "user",
            "can_write",
            "can_edit",
            "can_delete",
            "allowed_vendors",
            "throttle_scope",
            "valid_until",
        ]

    def clean(self):
        cleaned = super().clean()
        can_write = cleaned.get("can_write", False)
        can_edit = cleaned.get("can_edit", False)
        can_delete = cleaned.get("can_delete", False)
        allowed_vendors = cleaned.get("allowed_vendors", [])

        valid_until = cleaned.get("valid_until")
        if valid_until and valid_until <= timezone.now():
            raise ValidationError({"valid_until": "The valid_until date must be in the future."})

        if (can_write or can_edit or can_delete) and not allowed_vendors:
            raise ValidationError({
                "allowed_vendors": "If any of can_write, can_edit or can_delete is True, "
                                   "you must select at least one vendor."
            })

        return cleaned
