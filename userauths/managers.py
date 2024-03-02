from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .models import *


class CustomUserManager(BaseUserManager):
    def create_customer(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("role", 1)

        if extra_fields.get("role") != 1:
            raise ValueError("Superuser must have role of Global Admin")
        return self.create_customer(email, password, **extra_fields)

    def create_vendor(self, email, password, **extra_fields):
        extra_fields.setdefault("role", 2)

        if extra_fields.get("role") != 2:
            raise ValueError("Vendor must have role of Vendor")
        return self.create_customer(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)
