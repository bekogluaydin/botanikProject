from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("login", views.user_login, name="user_login"),
    path("register", views.user_register, name="user_register"),
    path('change-password', views.user_change_password, name='user_change_password'),
    path("logout", views.user_logout, name="user_logout"),

    # User Group
    path("user-groups/", views.user_group_list, name="user_group_list"),
    path("user-groups/create/", views.user_group_create, name="user_group_create"),
    path('user-groups/edit/<int:user_group_id>', views.user_group_edit, name='user_group_edit'),
    path('user-groups/delete/<int:user_group_id>', views.user_group_delete, name='user_group_delete'),

    # Table Permission Area
    path("table-permission-area/", views.table_permission_area_list, name="table_permission_area_list"),
]