import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm

@csrf_protect
def REGISTER(request):
    if request.method != "POST":
        return render(request, 'auth/register.html', {'form': CustomUserCreationForm()})

    form = CustomUserCreationForm(request.POST)
    if not form.is_valid():
        return render(request, 'auth/register.html', {'form': form})

    user = create_user(form)
    add_user_to_group(user, 'CTV')
    login_and_redirect(request, user)
    return redirect('/home')


def create_user(form):
    user = form.save(commit=False)
    user.username = form.cleaned_data.get('email').split("@")[0]
    user.save()
    return user


def add_user_to_group(user, group_name):
    group = Group.objects.get(name=group_name)
    group.user_set.add(user)


def login_and_redirect(request, user):
    request.session['user_id'] = user.id
    login(request, user)


@csrf_protect
def LOGIN(request):
    if request.method != 'POST':
        return render(request, 'auth/login.html')

    code = request.POST.get('code')
    password = request.POST.get('password')
    user = authenticate(request, code=code, password=password)

    if user is not None:
        request.session['user_id'] = user.username
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Invalid phone number or password.')
        return render(request, 'auth/login.html')


def LOGOUT(request):
    logout(request)
    return redirect('/home')
