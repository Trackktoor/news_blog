import cryptocode

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from .models import CustomUser
from .forms import UserRegistrationForm
from blog.secrets import KEY_FOR_HASH
from users import util


class check_verify_code(View):

    hash = None
    user_id = None
    
    def post(self, request, hash, user_id):    
        user = CustomUser.objects.get(id=user_id)

        if request.POST['verify_code'] == cryptocode.decrypt(self.kwargs['hash'], KEY_FOR_HASH):
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, 'news/home.html', )
        else:
            user.delete()
            return self.get(request, )

    def get(self, request):
        return render(request, 'registration/verify_code.html')

class Registrate(View):
    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            verify_code = util.send_verify_mail(user_form.cleaned_data['email']) 
            new_user.is_active = False
            new_user.save()
            return redirect('check_verify_code', hash=verify_code['hash_verify_code'], user_id=new_user.id)
        else:
            user_form = UserRegistrationForm()
            return render(request, 'registration/signup.html', {'form': user_form})

    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, 'registration/signup.html', {'form': user_form})

