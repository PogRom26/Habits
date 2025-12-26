from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать объект только его владельцу.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение для всех запросов (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем запись только владельцу объекта
        return obj.user == request.user


class IsPublicOrOwner(permissions.BasePermission):
    """
    Разрешение, позволяющее видеть публичные привычки всем,
    но редактировать только владельцу.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение публичных привычек всем
        if request.method in permissions.SAFE_METHODS and obj.is_public:
            return True

        # Разрешаем все действия владельцу
        return obj.user == request.user