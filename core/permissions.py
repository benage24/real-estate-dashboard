from rest_framework import permissions

class isSuperadminOrisManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        superUser=user.is_superuser
        admin=user.is_admin
        # check if user is superuser and admin and have full privilege of (CRUD)
        if user and admin and superUser :
            return True
        # check if user is admin and give privilege (CRU)
        if user and admin and request.method !='DELETE' :
            return True
        if user and admin and request.method != 'CREATE' and request.method != 'DELETE':
            return True
        return False

class isSuperadminOrisManagerRO(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        superUser=user.is_superuser
        admin=user.is_admin
        # check if user is superuser and admin and have full privilege of (CRUD)
        if user and admin and superUser :
            return True

        if user and admin and request.method != 'CREATE' and request.method != 'DELETE':
            return True
        return False


