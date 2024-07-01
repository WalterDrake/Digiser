import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import CustomUserCreationForm
from Digiser_ctv.services import add_row, count_row, find_id_with_username, send_zalo_oa_message_to_client
from django.contrib.auth.models import Group
# Create your views here.


@csrf_protect
def REGISTER(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set the username to email if necessary
            user.username = form.cleaned_data.get('username_zalo')
            user.save()  # Save the user instance
            group = Group.objects.get(name='CTV')
            group.user_set.add(user)
            doc_name = os.getenv("DOC_LIST").split(",")[0]
            cnt = count_row(doc_name, 0)
            user_dict = {
                "ID": "",
                "password": form.cleaned_data.get('password2'),
                "gmail": user.email
            }
            add_row(doc_name, 0, cnt, user_dict)
            user_id = find_id_with_username(form.cleaned_data.get('username_zalo'))
            if user_id['data'] != 'none':
                send_zalo_oa_message_to_client(user_id['data'], f"""Chúc mừng {request.POST.get('username_zalo')}. Bạn đã đăng ký tài khoản CTV thành công tại Digiser. Đăng nhập với số điện thoại {form.cleaned_data.get('phone_no')} và mật khẩu là {form.cleaned_data.get('password2')}""")
            login(request, user)
            return redirect('/home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html')


@csrf_protect
def LOGIN(request):
    if request.method == 'POST':
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        user = authenticate(request, username=phone_no, password=password)
        if user is not None:
            print(user.is_verified)
            request.session['user_id'] = user.id
            login(request, user) 
            # Replace 'home' with the name of your home URL pattern
            return redirect('home')
        else:
            messages.error(request, 'Invalid phone number or password.')

    return render(request, 'login.html')

def LOGOUT(request):
    logout(request)
    return redirect('/home')

