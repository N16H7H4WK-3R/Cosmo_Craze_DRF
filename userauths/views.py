from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .helper import get_tokens_for_user, send_email
from rest_framework.response import Response
from .models import Customer, Vendor, Admin
from rest_framework.views import APIView
from rest_framework import status
from .custom_permissions import *
from dotenv import load_dotenv
from .serializers import *
import threading

load_dotenv()


class CustomerRegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            contact_number = serializer.validated_data.get("contact_number")

            # Check if email already exists
            if Customer.objects.filter(email=email).exists():
                return Response(
                    {
                        "success": False,
                        "message": "Email already exists",
                        "email": ["Email already exists"],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if phone number already exists
            if Customer.objects.filter(contact_number=contact_number).exists():
                return Response(
                    {
                        "success": False,
                        "message": "Phone number already exists",
                        "contact_number": ["Phone number already exists"],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            customer = serializer.save()
            self.send_registration_email(serializer.validated_data["email"])
            tokens = get_tokens_for_user(customer)
            return Response(
                {
                    "success": True,
                    "message": "Successfully registered!",
                    "token": tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Registration failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def send_registration_email(self, email):
        subject = "Registration Successful"
        message = (
            "Welcome to our platform, you have successfully registered as a Customer"
        )
        threading.Thread(target=send_email, args=(email, subject, message)).start()


class VendorRegistrationAPIView(APIView):
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            contact_number = serializer.validated_data.get("contact_number")

            # Check if email already exists
            if Vendor.objects.filter(email=email).exists():
                return Response(
                    {
                        "success": False,
                        "message": "Email already exists",
                        "email": ["Email already exists"],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if phone number already exists
            if Vendor.objects.filter(contact_number=contact_number).exists():
                return Response(
                    {
                        "success": False,
                        "message": "Phone number already exists",
                        "contact_number": ["Phone number already exists"],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            vendor = serializer.save()
            self.send_registration_email(serializer.validated_data["email"])
            tokens = get_tokens_for_user(vendor)
            return Response(
                {
                    "success": True,
                    "message": "Successfully registered!",
                    "token": tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Registration failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def send_registration_email(self, email):
        subject = "Registration Successful"
        message = (
            "Welcome to our platform, you have successfully registered as a Vendor"
        )
        threading.Thread(target=send_email, args=(email, subject, message)).start()


class AdminRegistrationAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminAuthenticated)

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")

            # Check if email already exists
            if Admin.objects.filter(email=email).exists():
                return Response(
                    {
                        "success": False,
                        "message": "Email already exists",
                        "email": ["Email already exists"],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            admin = serializer.save()
            self.send_registration_email(serializer.validated_data["email"])
            tokens = get_tokens_for_user(admin)
            return Response(
                {
                    "success": True,
                    "message": "Successfully registered!",
                    "token": tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Registration failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def send_registration_email(self, email):
        subject = "Registration Successful"
        message = (
            "Welcome to our platform, you have successfully registered as an Admin"
        )
        threading.Thread(target=send_email, args=(email, subject, message)).start()


class FetchUserDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role == 3:
            customer = Customer.objects.get(pk=user.pk)
            customer_serializer = CustomerSerializer(customer)
            address_serializer = AddressSerializer(
                customer.address_set.all(), many=True
            )
            data = {
                "customer": customer_serializer.data,
                "addresses": address_serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        elif user.role == 2:
            vendor = Vendor.objects.get(pk=user.pk)
            vendor_serializer = VendorSerializer(vendor)
            return Response(vendor_serializer.data, status=status.HTTP_200_OK)
        elif user.role == 1:
            admin = Admin.objects.get(pk=user.pk)
            admin_serializer = AdminSerializer(admin)
            return Response(admin_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class EditCustomerProfile(APIView):
    permission_classes = (IsAuthenticated, IsCustomerAuthenticated)

    def patch(self, request):
        user = request.user
        customer = Customer.objects.get(pk=user.pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Profile updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "Profile update failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class EditVendorProfile(APIView):
    permission_classes = (IsAuthenticated, IsVendorAuthenticated)

    def patch(self, request):
        user = request.user
        vendor = Vendor.objects.get(pk=user.pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Profile updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "Profile update failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class EditAdminProfile(APIView):
    permission_classes = (IsAuthenticated, IsAdminAuthenticated)

    def patch(self, request):
        user = request.user
        admin = Admin.objects.get(pk=user.pk)
        serializer = AdminSerializer(admin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Profile updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "Profile update failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class BaseLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = None
    model = None

    def post(self, request):
        try:
            email = request.data["email"]
            password = request.data["password"]
            user = self.model.objects.get(email=email)
            if user.role == 3:
                if user.check_password(password):
                    tokens = get_tokens_for_user(user)
                    response = {
                        "success": True,
                        "message": "Login successful!",
                        "token": tokens,
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {
                        "success": False,
                        "message": "Wrong password!",
                        "error": "The password is incorrect for this customer",
                    }
                    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            if user.role == 2:
                if user.check_password(password):
                    tokens = get_tokens_for_user(user)
                    response = {
                        "success": True,
                        "message": "Login successful!",
                        "token": tokens,
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {
                        "success": False,
                        "message": "Wrong password!",
                        "error": "The password is incorrect for this vendor",
                    }
                    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            if user.role == 1:
                if user.check_password(password):
                    tokens = get_tokens_for_user(user)
                    response = {
                        "success": True,
                        "message": "Login successful!",
                        "token": tokens,
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {
                        "success": False,
                        "message": "Wrong password!",
                        "error": "The password is incorrect for this admin",
                    }
                    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            else:
                response = {
                    "success": False,
                    "message": "Login failed!",
                    "error": "The user is not a customer",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        except self.model.DoesNotExist:
            user = email
            user_type = self.model.__name__
            response = {
                "success": False,
                "message": "Login failed!",
                "error": f"The user with email {user} does not exist as {user_type}",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class CustomerLoginAPIView(BaseLoginAPIView):
    serializer_class = CustomerLoginSerializer
    model = Customer


class AdminLoginAPIView(BaseLoginAPIView):
    serializer_class = AdminLoginSerializer
    model = Admin


class VendorLoginAPIView(BaseLoginAPIView):
    serializer_class = VendorLoginSerializer
    model = Vendor


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {"success": True, "message": "Successfully logged out"},
                    status=status.HTTP_205_RESET_CONTENT,
                )
            except Exception as e:
                return Response(
                    {"success": False, "message": "Logout failed", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"success": False, "message": "Refresh token not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
