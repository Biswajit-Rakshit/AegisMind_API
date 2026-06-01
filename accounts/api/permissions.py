from rest_framework import permissions

class IsEmployee(permissions.BasePermission):
    '''Custom permission to allow only employees to access certain views'''

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'employee'