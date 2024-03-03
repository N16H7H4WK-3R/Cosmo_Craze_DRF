from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class IsAdminAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            raise PermissionDenied()

        # Check if the authenticated user has the required role
        required_roles = 1  # Update with your desired roles
        user = request.user
        if user.role == required_roles:
            return True
        raise PermissionDenied()


class IsVendorAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return PermissionDenied()

        # Check if the authenticated user has the required role
        required_roles = 2  # Update with your desired roles
        user = request.user
        if user.role == required_roles:
            return True
        return PermissionDenied()


class IsCustomerAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return PermissionDenied()

        # Check if the authenticated user has the required role
        required_roles = 3  # Update with your desired roles
        user = request.user
        if user.role == required_roles:
            return True
        return PermissionDenied()
