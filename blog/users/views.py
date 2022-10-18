from django.contrib.auth import login
import cryptocode
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.views import generic

from blog.secrets import KEY_FOR_HASH

from users import util

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def Registrate(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            verify_code = util.send_verify_mail(user_form.cleaned_data['email']) 
            new_user.is_active = False
            new_user.save()
            return redirect(check_verify_code, hash=verify_code['hash_verify_code'], user_id=new_user.id)
        else:
            user_form = UserRegistrationForm()
            return render(request, 'registration/signup.html', {'form': user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': user_form})

def check_verify_code(request, hash, user_id):
    if request.method == 'POST':        
        user = CustomUser.objects.get(id=user_id)

        if request.POST['verify_code'] == cryptocode.decrypt(hash, KEY_FOR_HASH):
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, 'news/home.html')
        else:
            user.delete()
            return render(request, 'registration/signup.html')
    else:
        return render(request, 'registration/verify_code.html')

    
