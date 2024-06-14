import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import CustomUserCreationForm
from Digiser_ctv.services import add_row, count_row

# Create your views here.


@csrf_protect
def REGISTER(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set the username to email if necessary
            user.username = form.cleaned_data.get('email').split("@")[0]
            user.save()  # Save the user instance
            doc_name = os.getenv("DOC_LIST").split(",")[0]
            cnt = count_row(doc_name, 0)
            user_dict = {
                "ID": "DGS" + str(cnt),
                "password": form.cleaned_data.get('password2'),
                "gmail": user.email
            }
            add_row(doc_name, 0, cnt, user_dict)
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
        print(user)
        if user is not None:
            login(request, user)
            # Replace 'home' with the name of your home URL pattern
            return redirect('home')
        else:
            messages.error(request, 'Invalid phone number or password.')

    return render(request, 'login.html')


def LOGOUT(request):
    logout(request)
    return redirect('/home')

