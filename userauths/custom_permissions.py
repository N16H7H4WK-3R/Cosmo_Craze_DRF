from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class IsAdminAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            raise PermissionDenied()

        required_roles = 1
        user = request.user
        if user.role == required_roles:
            return True
        raise PermissionDenied()


class IsVendorAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return PermissionDenied()

        required_roles = 2
        user = request.user
        if user.role == required_roles:
            return True
        raise PermissionDenied()


class IsCustomerAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return PermissionDenied()

        required_roles = 3
        user = request.user
        if user.role == required_roles:
            return True
        raise PermissionDenied()
