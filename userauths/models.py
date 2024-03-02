from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    VENDOR = 2
    CUSTOMER = 3

    ROLE_CHOICES = ((ADMIN, "Admin"), (VENDOR, "Vendor"), (CUSTOMER, "Customer"))

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True, default=CUSTOMER
    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class Admin(User):
    admin_id = ShortUUIDField(
        unique=True, length=10, max_length=20, prefix="adm", alphabet="abcdefgh12345"
    )
    contact_number = models.CharField(max_length=15, default="none")
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Admins"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class Vendor(User):
    vendor_id = ShortUUIDField(
        unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345"
    )
    vendor_title = models.CharField(max_length=100)
    vendor_image = models.ImageField(
        upload_to="vendor_images/", default="vendor_images/default.jpg"
    )
    vendor_description = models.TextField(null=True, blank=True)
    # change
    vendor_address = models.CharField(max_length=100, default="N/A , India")
    contact_number = models.CharField(max_length=15, default="none")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_images(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % (self.vendor_image.url)
        )

    def __str__(self):
        return self.vendor_title


class Customer(User):
    customer_id = ShortUUIDField(
        unique=True, length=10, max_length=20, prefix="cus", alphabet="abcdefgh12345"
    )
    customer_image = models.ImageField(upload_to="customer_images/")
    contact_number = models.CharField(max_length=15, default="none", unique=True)

    class Meta:
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    postal_code = models.CharField(max_length=20)
    status = models.BooleanField(default=False)

    class meta:
        verbose_name_plural = "Address"
