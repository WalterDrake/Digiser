from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import CustomUserCreationForm
# Create your views here.


def REGISTER(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set the username to email if necessary
            user.username = form.cleaned_data.get('email')
            user.save()  # Save the user instance
            login(request, user)
            return redirect('home')
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
            return redirect('home')  # Replace 'home' with the name of your home URL pattern
        else:
            messages.error(request, 'Invalid phone number or password.')

    return render(request, 'login.html')


def LOGOUT(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')