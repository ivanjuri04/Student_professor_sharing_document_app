from django.http import HttpResponse
from django.shortcuts import redirect
from collections import UserDict

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
       ## user_role=request.user.role
      
        if request.user.is_authenticated  : #ako ovo ne nepravi uzima view function koja moze bit bilo koja  funkcija i nju prikazuje
            return redirect('doma')         ##and user_role != 'admin'  
        else:
            return view_func(request,*args,**kwargs)  
    return wrapper_func


def allowd_users(allowd_roles=[]):
    def decorator(view_function):
        def wrapper_func(request,*args,**kwargs):
            group =None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name

            if group in allowd_roles:
                return view_function(request,*args,**kwargs)
            else:
                return HttpResponse('You are not authorised')
        return wrapper_func
    return decorator
