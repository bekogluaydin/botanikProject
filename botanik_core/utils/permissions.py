from django.http import HttpResponseForbidden
from functools import wraps

def user_can_view(table_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Giriş yapmanız gerekiyor.")

            if hasattr(request.user, "userpermission"):
                can_view = request.user.userpermission.can_view_tables.filter(name=table_name).exists()
                if can_view:
                    return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("Bu tabloyu görüntüleme yetkiniz yok.")
        return _wrapped_view
    return decorator


def user_can_add(table_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Giriş yapmanız gerekiyor.")

            if hasattr(request.user, "userpermission"):
                can_add = request.user.userpermission.can_add_tables.filter(name=table_name).exists()
                if can_add:
                    return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("Bu tabloya kayıt yapma yetkiniz yok.")
        return _wrapped_view
    return decorator