import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import Group

def add_user_to_group(user, group_name):
    group = Group.objects.get(name=group_name)
    group.user_set.add(user)


def login_and_redirect(request, user):
    request.session['user_code'] = user.code
    login(request, user)


@csrf_protect
def LOGIN(request):
    if request.method != 'POST':
        return render(request, 'auth/login.html')

    code = request.POST.get('code')
    password = request.POST.get('password')
    user = authenticate(request, code=code, password=password)

    if user is not None:
        request.session['user_code'] = user.code
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Sai mã ctv hoặc mật khẩu.')
        return render(request, 'auth/login.html')


def LOGOUT(request):
    logout(request)
    return redirect('/home')



