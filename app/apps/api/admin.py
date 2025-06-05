from django.contrib import admin
from apps.api.models import APIToken
from apps.api.forms import APITokenForm
import copy
#
# ─── API TOKEN ADMIN ───────────────────────────────────────────────────────────────
#
@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    form = APITokenForm

    list_display = (
        "id",
        "name",
        "user",
        "can_write",
        "can_edit",
        "can_delete",
        "throttle_scope",
        "valid_until",
        "is_valid",
        "created_at",
        "updated_at",
    )
    list_select_related = ("user",)
    raw_id_fields = ("user",)

    date_hierarchy = "valid_until"
    readonly_fields   = ("key", "is_valid", "created_at", "updated_at")
    ordering = ("-created_at",)

    search_fields = ("name", "user__username")
    list_filter = ("can_write", "can_edit", "can_delete", "throttle_scope", "valid_until")
    filter_horizontal = ("allowed_vendors",)


    fieldsets = (
        (None, {
            "fields": (
                "name",
                "key",
                "user",
                "can_write",
                "can_edit",
                "can_delete",
                "allowed_vendors",
                "throttle_scope",
                "valid_until",
            )
        }),
        ("Metadata", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(copy.deepcopy(self.readonly_fields))
        if obj:
            readonly += ["name", "user", "can_write", "can_edit", "can_delete", 
                         "allowed_vendors", "throttle_scope", "valid_until"]
        return readonly

    def save_model(self, request, obj, form, change):

        is_new = not change
        super().save_model(request, obj, form, change)

        if is_new:
            jwt_token = obj.generate_jwt()
            self.message_user(
                request,
                f"JWT (expires {obj.valid_until:%Y-%m-%d %H:%M}) for token '{obj.name}':\n{jwt_token}\n"
            )

    def is_valid(self, obj):
        return obj.is_valid
    
    is_valid.boolean = True
    is_valid.short_description = "Still Valid?"
