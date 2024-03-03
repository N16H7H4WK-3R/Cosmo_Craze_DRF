from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from email.mime.text import MIMEText
import threading
import smtplib
from .models import Customer, Vendor, Admin
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .helper import get_tokens_for_user
from .custom_permissions import (
    IsAdminAuthenticated,
    IsVendorAuthenticated,
    IsCustomerAuthenticated,
)


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
    permission_classes = (IsAdminAuthenticated,)

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


def send_email(to_email, subject, message):
    # Configure Gmail SMTP server details
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "aryan014kumar@gmail.com"
    smtp_password = "fqrvdrpxsvuwykvc"
    sender_email = "aryan014kumar@gmail.com"

    # Create a MIME message
    msg = MIMEText(message)
    msg["Subject"] = subject[0]
    msg["From"] = sender_email
    msg["To"] = to_email

    # Send the email
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
