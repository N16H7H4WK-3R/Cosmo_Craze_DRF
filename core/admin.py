from django.contrib import admin
from core.models import (
    Product,
    Category,
    CartOrder,
    CartOrderItems,
    ProductImages,
    ProductReview,
    wishlist,
)
from django.utils.safestring import mark_safe


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = (
        "vendor",
        "product_title",
        "product_image",
        "product_price",
        "featured",
        "product_status",
    )
    readonly_fields = ("product_id",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_title", "category_image")
    readonly_fields = ("category_id",)


class CartOrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "price", "paid_status", "order_date", "product_status")


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "invoice_no",
        "item",
        "image",
        "quantity",
        "price",
        "total",
    )
    readonly_fields = ("invoice_no",)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "review", "rating")


class WishlistAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "date")


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(wishlist, WishlistAdmin)
