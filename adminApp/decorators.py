from functools import wraps
from django.http import HttpResponseForbidden
from core.models import *




def role_required(*role_names):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            role_ids = Role.objects.filter(name__in=role_names).values_list('id', flat=True)
            user_role_ids = request.user.role.values_list('id', flat=True) # افترض ان لديك علاقة بين مستخدم والأدوار

            if any(role_id in user_role_ids for role_id in role_ids):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")

        return wrapper
    return decorator