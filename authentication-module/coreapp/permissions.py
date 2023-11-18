from rest_framework.permissions import BasePermission


class IsApproved(BasePermission):
    """
    Allows access only to approved users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_approved)
