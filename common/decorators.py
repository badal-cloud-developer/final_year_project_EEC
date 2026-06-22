from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Custom decorator to restrict access based on user roles.
    Only users with the specified roles are allowed to access the view.
    """
    def decorator(view_func):
        @login_required  # Ensure the user is authenticated
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Check if the user's role is in the allowed roles
                if request.user.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied  # Raise 403 if the user doesn't have the correct role
            else:
                raise PermissionDenied  # Raise 403 if the user is not authenticated

        return _wrapped_view

    return decorator
