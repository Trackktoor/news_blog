from tkinter import N
from django import dispatch
from .models import *
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import render

from django.shortcuts import  redirect, reverse

class VerificationUserMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request,  *args, **kwargs)
        else:
            return redirect(reverse('login'))

class ViewPostsMixin(View):
    template_name = None
    order_by = None

    def get(self, request, page_paginator=1):

        posts_paginate = Paginator(Post.objects.order_by(self.order_by), 5)
        page = posts_paginate.page(page_paginator)
        
        return render(request, self.template_name, context = {'posts': page.object_list, 'page': page})
    

def get_client_ip(request):
    x_forwared_for = request.META.get('HTTP_X_FORWARED_FOR')
    if x_forwared_for:
        ip = x_forwared_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip