from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ProfileForm
from users.forms import LoginUserForm, RegisterUserForm

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    success_url = reverse_lazy('home')
    
class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy('users:login')

@login_required
def update_avatar(request):
        if request.method == 'POST' and request.FILES.get('avatar'):
            profile = request.user.profile  # Получаем профиль текущего пользователя
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'avatar_url': profile.avatar.url})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def update_bio(request):
    if request.method == 'POST':
        profile = request.user.profile
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'bio': form.cleaned_data['bio']})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


