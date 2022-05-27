from rest_framework.permissions import BasePermission
from utils.jwt import decode
from jwt import DecodeError


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user)
