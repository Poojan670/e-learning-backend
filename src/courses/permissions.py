from rest_framework.permissions import BasePermission


class IsOwnerAuth(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        if request.user and request.user.is_superuser == True:
            return True
        return False

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        if request.user and request.user.is_superuser == True:
            return True
        return False


class ModelViewSetsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "PUT", "DELETE"]:
            return False
        if request.user and request.user.is_superuser == True:
            return True
        return True


class ReviewReplyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.course.seller.user == request.user:
            return True
        if request.user and request.user.is_superuser == True:
            return True
        return False


class AnnouncementObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.instrutor == request.user:
            return True
        if request.user and request.user.is_superuser == True:
            return True
        return False
