from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from sitewomen import settings
from .forms import LoginUserForm,  RegisteruserForm, ProfileUsersForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title':'Авторизация'}
    

    # def get_success_url(self): 
    #     return reverse_lazy('home')

class RegisterUser(CreateView):
    form_class = RegisteruserForm
    template_name= 'users/register.html'
    extra_context = {'title':'Регистрация'}
    success_url= reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUsersForm
    template_name = 'users/profile.html'
    extra_context = {'title':'Профиль пользователя','default_image':settings.DEFAULT_USER_IMAGE,}

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile',)
    
    def form_valid(self, form):
        print("Сохраняем:", form.cleaned_data)
        return super().form_valid(form)
    

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = 'users/password_change_form.html'