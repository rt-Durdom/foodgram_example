from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAuthor(permissions.BasePermission):

    # # Определяет права на уровне запроса и пользователя
    # def has_permission(self, request, view):
    #     return True

    # Определяет права на уровне объекта
    def has_object_permission(self, request, view, recipe):
        if request.method in SAFE_METHODS:
            return True
        # if request.user.is_superuser:
        #     return True
        return request.user == recipe.author
