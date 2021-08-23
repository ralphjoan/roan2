from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from .models import *

def admin_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = Group.objects.get(user = request.user)
        if group.name == 'admin_owner':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_func

 
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page!')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
                group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('main/home.html')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func


