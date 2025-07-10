from django import template
register = template.Library()

@register.filter
def can_view_table(user, table_name):
    if user.is_superuser or user.is_staff:
        return True
    try:
        return user.userpermission.can_view_tables.filter(name=table_name, is_active=True).exists()
    except:
        return False