from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.


def register(request):
    # if request.method == "POST":
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         # Set the username to email if necessary
    #         user.username = form.cleaned_data.get('email')
    #         user.save()  # Save the user instance
    #         login(request, user)
    #         return redirect('home')
    # else:
    #     form = CustomUserCreationForm()
    return render(request, 'register.html')


def login(request):
    # if request.method == "POST":
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('home')  # Redirect to a success page.
    # else:
    #     form = AuthenticationForm()
    return render(request, 'login.html')


def logout(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')