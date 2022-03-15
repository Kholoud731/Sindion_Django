from textwrap import wrap
from tokenize import group
from django.core.exceptions import PermissionDenied



def employee_only(view_func):
    def wrap(request, *args, **kwargs):

        if request.user.groups.exists():

            if request.user.groups.all()[0].name == "employee":
                return view_func(request, *args, **kwargs)
        else:
                raise PermissionDenied
    return wrap


# def allowed_users(allowed_roles=[]):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name

#             if group in allowed_roles:
#                 return view_func(request,*args, **kwargs)
#             else:
#                 raise PermissionDenied
#         return wrapper_func
#     return decorator