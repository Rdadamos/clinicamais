from functools import wraps
from django.http import HttpResponseRedirect
from django.contrib import messages

def attendant_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            attendant = request.user.attendant
            return function(request, *args, **kwargs)
        except:
            messages.error(request, 'Acesso não permitido')
            return HttpResponseRedirect('/home/')
    return wrap

def anonimous_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Usuário já está logado')
            return HttpResponseRedirect('/home/')
    return wrap
