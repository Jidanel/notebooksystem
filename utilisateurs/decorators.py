from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func



def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.profilutilisateur.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'utilisateurs/permission_denied.html')
        return wrap
    return decorator
