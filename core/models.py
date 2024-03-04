from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from userauths.models import User, Vendor, Customer


STATUS_CHOICES = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    ("1", "★ ✮ ✮ ✮ ✮"),
    ("2", "★ ★ ✮ ✮ ✮"),
    ("3", "★ ★ ★ ✮ ✮"),
    ("4", "★ ★ ★ ★ ✮"),
    ("5", "★ ★ ★ ★ ★"),
)


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class Category(models.Model):
    category_id = ShortUUIDField(
        unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345"
    )
    category_title = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to="category_images/")

    class meta:
        verbose_name_plural = "Categories"

    def category_images(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % (self.category_image.url)
        )

    def __str__(self):
        return self.category_title


class Product(models.Model):
    product_id = ShortUUIDField(
        unique=True,
        length=10,
        max_length=20,
        prefix="pro",
        alphabet="abcdefgh12345",
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product_title = models.CharField(max_length=100)
    product_image = models.ImageField(
        upload_to="user_directory_path/", default="product.jpg"
    )
    product_description = models.TextField(null=True, blank=True, default="N/A")
    product_price = models.DecimalField(
        max_digits=999999999999999999, decimal_places=2, default=1999.00
    )
    product_old_price = models.DecimalField(
        max_digits=999999999999999999, decimal_places=2, default=2999.00
    )
    product_specifications = models.TextField(null=True, blank=True)

    product_status = models.CharField(
        max_length=10, choices=STATUS, default="in_review"
    )

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(
        unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890"
    )

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class meta:
        verbose_name_plural = "Products"

    def product_images(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % (self.product_image.url)
        )

    def __str__(self):
        return self.product_title

    def get_percentage(self):
        new_price = (self.product_price / self.product_old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class meta:
        verbose_name_plural = "Product Images"


################################### Cart, Order, OrderItems and address ########################################
################################### Cart, Order, OrderItems and address ########################################
################################### Cart, Order, OrderItems and address ########################################
################################### Cart, Order, OrderItems and address ########################################


class CartOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(
        max_digits=999999999999999999, decimal_places=2, default=1000.00
    )
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="processing"
    )

    class meta:
        verbose_name_plural = "Orders"
        ordering = ["-order_date"]

    def __str__(self):
        return f"Order #{self.id}"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(
        max_digits=999999999999999999, decimal_places=2, default=1000.00
    )
    total = models.DecimalField(
        max_digits=999999999999999999, decimal_places=2, default=1000.00
    )

    class meta:
        verbose_name_plural = "Cart Order Items"

    def __str__(self):
        return self.item

    def order_image(self):
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" />' % (self.image)
        )


################################### Product Review, Wishlists, Address ########################################
################################### Product Review, Wishlists, Address ########################################
################################### Product Review, Wishlists, Address ########################################
################################### Product Review, Wishlists, Address ########################################


class ProductReview(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField(null=True, blank=True)
    rating = models.CharField(max_length=50, choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.product_title

    def get_rating(self):
        return self.rating


class wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.product_title
