from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer, Vendor, Admin, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["user"]


class CustomerSerializer(serializers.ModelSerializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    address = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "password",
            "address",
            "access",
            "refresh",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        address_data = validated_data.pop("address", [])
        user = Customer.objects.create_customer(**validated_data)
        for address_item in address_data:
            Address.objects.create(user=user, **address_item)
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        validation = {
            "access": access_token,
            "refresh": refresh_token,
            "email": user.email,
        }
        update_last_login(None, user)
        return validation and user


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "vendor_id",
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "password",
            "vendor_title",
            "vendor_description",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        auth_user = Vendor.objects.create_vendor(**validated_data)
        return auth_user


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            "admin_id",
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        auth_user = Admin.objects.create_superuser(**validated_data)
        return auth_user


class BaseLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    role = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        return self.get_validation_data(user)

    def get_validation_data(self, user):
        raise NotImplementedError(
            "Subclasses must implement get_validation_data method."
        )


class UserLoginSerializer(BaseLoginSerializer):
    user_model = None

    def get_validation_data(self, user):
        if not isinstance(user, self.user_model):
            raise serializers.ValidationError("Invalid login credentials")
        access_token, refresh_token = self.generate_tokens(user)
        return {
            "access": access_token,
            "refresh": refresh_token,
            "email": user.email,
            "role": user.role,
        }


class CustomerLoginSerializer(UserLoginSerializer):
    user_model = Customer


class AdminLoginSerializer(UserLoginSerializer):
    user_model = Admin


class VendorLoginSerializer(UserLoginSerializer):
    user_model = Vendor
