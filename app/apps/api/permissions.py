# apps/api/permissions.py

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from apps.api.models import APIToken
from django.utils import timezone

class TokenPermission(permissions.BasePermission):
    """
    - Safe (read‐only) methods (GET/HEAD/OPTIONS) are always allowed.
    - For POST:
        • JWT required. Check token exists and not expired.
        • token.can_write must be True.
        • If 'vendor' provided in payload, it must be in token.allowed_vendors.
    - For PUT/PATCH:
        • JWT required. Check token exists and not expired.
        • token.can_edit must be True.
        • The existing object's vendor must be in token.allowed_vendors.
    - For DELETE:
        • JWT required. Check token exists and not expired.
        • token.can_delete must be True.
        • The existing object's vendor must be in token.allowed_vendors.
    """

    def _get_api_token(self, token_payload):
        """
        Look up APIToken row by token_key. Check expiration (valid_until).
        Raises PermissionDenied on any failure.
        """
        token_key = token_payload.get("token_key")
        if not token_key:
            raise PermissionDenied("Malformed token: missing token_key.")

        try:
            api_token = APIToken.objects.get(key=token_key)
        except APIToken.DoesNotExist:
            raise PermissionDenied("Token has been revoked or does not exist.")

        valid_until_ts = token_payload.get("valid_until")
        if not valid_until_ts:
            raise PermissionDenied("Malformed token: missing expiration.")
        if timezone.now().timestamp() >= valid_until_ts:
            raise PermissionDenied("Token has expired.")

        return api_token

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        token_payload = request.auth
        if not token_payload:
            raise NotAuthenticated("A valid JWT is required for write/edit/delete operations.")

        api_token = self._get_api_token(token_payload)

        if request.method == "POST":
            if not api_token.can_write:
                raise PermissionDenied("This token does not have create (POST) permissions.")
            vendor_id = request.data.get("vendor")
            if vendor_id is not None:
                try:
                    vendor_id = int(vendor_id)
                except (ValueError, TypeError):
                    raise PermissionDenied("Invalid vendor ID.")
                if not api_token.allowed_vendors.filter(id=vendor_id).exists():
                    raise PermissionDenied("You may not create objects for that vendor.")
            return True

        if request.method in ["PUT", "PATCH"]:
            if not api_token.can_edit:
                raise PermissionDenied("This token does not have edit (PUT/PATCH) permissions.")
            return True

        if request.method == "DELETE":
            if not api_token.can_delete:
                raise PermissionDenied("This token does not have delete (DELETE) permissions.")
            return True

        raise PermissionDenied(f"Method {request.method} not allowed.")

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        token_payload = request.auth
        api_token = self._get_api_token(token_payload)

        if request.method in ["PUT", "PATCH"]:
            if not api_token.can_edit:
                raise PermissionDenied("This token does not have edit permissions.")
            obj_vendor = getattr(obj, "vendor", None)
            if obj_vendor and not api_token.allowed_vendors.filter(id=obj_vendor.id).exists():
                raise PermissionDenied("You may not edit objects for that vendor.")
            return True

        if request.method == "DELETE":
            if not api_token.can_delete:
                raise PermissionDenied("This token does not have delete permissions.")
            obj_vendor = getattr(obj, "vendor", None)
            if obj_vendor and not api_token.allowed_vendors.filter(id=obj_vendor.id).exists():
                raise PermissionDenied("You may not delete objects for that vendor.")
            return True

        return True
