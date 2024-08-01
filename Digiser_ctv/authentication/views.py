import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from Digiser_ctv.services import update_row, count_row


@csrf_protect
def REGISTER(request):
    if request.method != "POST":
        return render(request, 'register.html', {'form': CustomUserCreationForm()})

    form = CustomUserCreationForm(request.POST)
    if not form.is_valid():
        return render(request, 'register.html', {'form': form})

    user = create_user(form)
    add_user_to_group(user, 'CTV')
    update_user_data(user, form)
    login_and_redirect(request, user)
    return redirect('/home')


def create_user(form):
    user = form.save(commit=False)
    user.username = form.cleaned_data.get('email').split("@")[0]
    user.row = count_row(os.getenv("DOC_LIST").split(",")[0], 0)
    user.save()
    return user


def add_user_to_group(user, group_name):
    group = Group.objects.get(name=group_name)
    group.user_set.add(user)


def update_user_data(user, form):
    doc_name = os.getenv("DOC_LIST").split(",")[0]
    user_dict = {
        "ID": user.code_ctv,
        "password": form.cleaned_data.get('password2'),
        "gmail": user.email,
        "phone": user.phone_no,
        "birthday": user.birthday,
        "full name": user.full_name,
        "address": user.address,
        "qualification": user.qualification,
        "identification": user.identification,
        "identification address": user.identification_address,
        "note": user.note,
        "role": user.role,
        "account number": user.account_number,
        "bank name": user.bank_name,
        "branch": user.branch,
        "owner": user.owner,
        "code bank": user.code_bank
    }
    update_row(doc_name, 0, user.row, user_dict)


def login_and_redirect(request, user):
    request.session['user_id'] = user.id
    login(request, user)


@csrf_protect
def LOGIN(request):
    if request.method != 'POST':
        return render(request, 'login.html')

    phone_no = request.POST.get('phone_no')
    password = request.POST.get('password')
    user = authenticate(request, username=phone_no, password=password)

    if user is not None:
        request.session['user_id'] = user.id
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Invalid phone number or password.')
        return render(request, 'login.html')


def LOGOUT(request):
    logout(request)
    return redirect('/home')



