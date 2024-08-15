from django.contrib import admin
from image_app.models import User, Interaction, Image

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile_number", "is_verified")
    search_fields = ("name", "mobile_number")
    list_filter = ("is_verified",)
    ordering = ("name",)
    fieldsets = ((None, {"fields": ("mobile_number", "name", "otp", "is_verified")}),)


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ("user", "image_name", "action", "timestamp")
    list_filter = ("action", "timestamp")
    search_fields = ("user__name", "image_name")
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    search_fields = ("name",)
    ordering = ("name",)
