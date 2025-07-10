from django.http import HttpResponseForbidden
from functools import wraps

# Sayfaya erişmek için yetki kontrolü yapılıyor. Eğer görme, ekleme yetkisi yoksa uyarı verip belirtilen sayfaya yönlendirme yapıyor.
def has_permission_to_view(user, table_name):
    if user.is_superuser or user.is_staff:
        return True

    if not hasattr(user, "userpermission"):
        return False
    return user.userpermission.can_view_tables.filter(name=table_name).exists()


def has_permission_to_add(user, table_name):
    if user.is_superuser or user.is_staff:
        return True
    
    if not hasattr(user, "userpermission"):
        return False
    return user.userpermission.can_add_tables.filter(name=table_name).exists()



# Decorator ile sayfaya erişmek için yetki kontrolü yapılıyor. Eğer görme, ekleme yetkisi yoksa uyarı verip belirtilen sayfaya yönlendirme yapıyor.
# def user_can_view(table_name):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.is_authenticated:
#                 return HttpResponseForbidden("Giriş yapmanız gerekiyor.")

#             if hasattr(request.user, "userpermission"):
#                 can_view = request.user.userpermission.can_view_tables.filter(name=table_name).exists()
#                 if can_view:
#                     return view_func(request, *args, **kwargs)

#             return HttpResponseForbidden("Bu tabloyu görüntüleme yetkiniz yok.")
#         return _wrapped_view
#     return decorator


# def user_can_add(table_name):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.is_authenticated:
#                 return HttpResponseForbidden("Giriş yapmanız gerekiyor.")

#             if hasattr(request.user, "userpermission"):
#                 can_add = request.user.userpermission.can_add_tables.filter(name=table_name).exists()
#                 if can_add:
#                     return view_func(request, *args, **kwargs)

#             return HttpResponseForbidden("Bu tabloya kayıt yapma yetkiniz yok.")
#         return _wrapped_view
#     return decorator