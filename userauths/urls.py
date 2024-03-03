from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import (
    CustomerRegistrationAPIView,
    VendorRegistrationAPIView,
    AdminRegistrationAPIView,
    CustomerLoginAPIView,
    AdminLoginAPIView,
    VendorLoginAPIView,
    FetchUserDetails,
    EditAdminProfile,
    EditCustomerProfile,
    EditVendorProfile,
    LogoutAPIView,
)

urlpatterns = [
    path("token/obtain/", jwt_views.TokenObtainPairView.as_view(), name="token_create"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "register/customer/",
        CustomerRegistrationAPIView.as_view(),
        name="customer-register",
    ),
    path(
        "register/vendor/", VendorRegistrationAPIView.as_view(), name="vendor-register"
    ),
    path("register/admin/", AdminRegistrationAPIView.as_view(), name="admin-register"),
    path("login/customer/", CustomerLoginAPIView.as_view(), name="customer-login"),
    path("login/admin/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("login/vendor/", VendorLoginAPIView.as_view(), name="vendor-login"),
    path("fetch/data/", FetchUserDetails.as_view(), name="fetch-user-data"),
    path("edit/admin/", EditAdminProfile.as_view(), name="edit-admin-profile"),
    path("edit/customer/", EditCustomerProfile.as_view(), name="edit-customer-profile"),
    path("edit/vendor/", EditVendorProfile.as_view(), name="edit-vendor-profile"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
