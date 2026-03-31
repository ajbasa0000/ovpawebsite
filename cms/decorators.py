from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def content_manager_required(view_func):
    """
    Decorator for views that checks if the user is a superuser or 
    belongs to the 'Staff Content Manager' group.
    """
    def check_user(user):
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name='Staff Content Manager').exists()

    return user_passes_test(check_user)(view_func)
