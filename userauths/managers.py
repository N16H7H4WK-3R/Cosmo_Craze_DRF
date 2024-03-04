from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_customer(self, email, password, **extra_fields):
        from .models import Customer

        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)

        customer = Customer(email=email, **extra_fields)
        customer.set_password(password)
        customer.save(using=self._db)
        return customer

    def create_superuser(self, email, password, **extra_fields):
        from .models import Admin

        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("role", 1)

        if extra_fields.get("role") != 1:
            raise ValueError("Superuser must have role of Global Admin")

        admin = Admin(email=email, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_vendor(self, email, password, **extra_fields):
        from .models import Vendor

        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)

        extra_fields.setdefault("role", 2)

        if extra_fields.get("role") != 2:
            raise ValueError("Vendor must have role of Vendor")

        vendor = Vendor(email=email, **extra_fields)
        vendor.set_password(password)
        vendor.save(using=self._db)
        return vendor

    def get_by_natural_key(self, email):
        return self.get(email=email)
