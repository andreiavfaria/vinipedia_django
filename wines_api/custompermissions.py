from rest_framework import permissions


class IsCurrentUserAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # The method is a safe method
            return True
        else:
        # The method isn't a safe method
        # Only owners are granted permissions for unsafe methods
            return obj.user == request.user


class IsCurrentUserAdminOrOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # The method is a safe method
            return True
        elif request.user.is_staff:
            return True
        else:
        # The method isn't a safe method
        # Only owners are granted permissions for unsafe methods
            return obj.user == request.user
