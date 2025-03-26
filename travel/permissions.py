from rest_framework import permissions

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow admins or the owner of the object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admins or the owner of the snippet.
        return obj.owner == request.user or request.user.is_staff
