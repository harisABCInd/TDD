from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """ Custom permission to only allow the owner to read and write """

    def has_object_permission(self, request, view, obj):
        return obj == request.user