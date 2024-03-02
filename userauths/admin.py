from django.contrib import admin
from .models import Admin, Vendor, Customer, User, Address


class AddressAdmin(admin.StackedInline):
    model = Address


class AllUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "role",
        "is_active",
        "created_at",
    )
    readonly_fields = ("created_at", "updated_at", "password")
    list_display_links = ("email", "id")


class AdminAdmin(admin.ModelAdmin):
    inlines = [AddressAdmin]
    list_display = ("email", "admin_id", "contact_number")
    readonly_fields = ("created_at", "updated_at", "password")


class VendorAdmin(admin.ModelAdmin):
    inlines = [AddressAdmin]
    list_display = (
        "email",
        "vendor_id",
        "vendor_title",
        "contact_number",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "is_superuser",
        "is_staff",
        "password",
    )


class CustomerAdmin(admin.ModelAdmin):
    inlines = [AddressAdmin]
    list_display = (
        "email",
        "customer_id",
        "created_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "is_superuser",
        "is_staff",
        "password",
    )


admin.site.register(User, AllUserAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Customer, CustomerAdmin)
