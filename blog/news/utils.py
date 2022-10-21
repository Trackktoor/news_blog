from django import dispatch
from .models import *
from django.views import View

from django.shortcuts import  redirect, reverse

class VerificationUserMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request,  *args, **kwargs)
        else:
            return redirect(reverse('login'))
    

def get_client_ip(request):
    x_forwared_for = request.META.get('HTTP_X_FORWARED_FOR')
    if x_forwared_for:
        ip = x_forwared_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip