from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from authentication.forms import CustomUserInfoChangeForm, CustomUserBankChangeForm
from django.db.models import Q
from authentication.models import CustomUser, LoginLog

from .utils import *

@login_required
def home(request):
    if request.method == 'GET':
        return handle_get_request(request)

def handle_get_request(request):
    user_code = request.session.get('user_code')
    user = get_object_or_404(CustomUser, code=user_code)
    if checkManager(user):
        return redirect('home_admin')
    
    total_salary = statistic_salary(user)
    total_project_details = statistic_project(user)
    context = {
        'total_project_details' : total_project_details,
        'total_salary' : total_salary
    }
    return render(request, 'pages/dashboard.html', context)


@login_required
def system(request):
    return render(request, 'pages/system.html')


@login_required
def wiki(request):
    return render(request, 'pages/wiki.html')


@login_required
def courses(request):
    return render(request, 'pages/courses.html')


@login_required
def info(request):
    user_code = request.session.get('user_code')
    user = get_object_or_404(CustomUser, code=user_code)
    if request.method == 'POST':
        return handle_info_post(request, user)
    elif user.is_verified:
        return handle_info_get(request, user)
    else:
        return redirect('/home')


def handle_info_post(request, user):
    form_type = request.POST.get('form_type')
    if form_type == 'personal_info':
        FormClass = CustomUserInfoChangeForm
    elif form_type == 'bank_info':
        FormClass = CustomUserBankChangeForm
    else:
        return render(request, 'pages/info.html', get_user_context(user))

    form = FormClass(request.POST, instance=request.user)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        return render(request, 'pages/info.html', get_user_context(user))
    return render(request, 'pages/info.html', get_user_context(user))


def handle_info_get(request, user):
    return render(request, 'pages/info.html', get_user_context(user))


def show_data_insert(request):
    user_code = request.session.get('user_code')
    user = get_object_or_404(CustomUser, code=user_code)


    filter_user = Q(inserter=user)
    data, package_detail_dict, documents_dict = get_package_data(filter_user)
    
    packages = build_package_info(user, data, package_detail_dict, documents_dict)

    if (request.body):
        return render(request, 'pages/insert.html', {'packages': filter_packages(request, packages)})                                           
    return render(request, 'pages/insert.html', {'packages': packages})

def show_data_check(request):
    user_code = request.session.get('user_code')
    user = get_object_or_404(CustomUser, code=user_code)

    filter_user = Q(checker_1=user) | Q(checker_2=user)
    data, package_detail_dict, documents_dict = get_package_data(filter_user)
    
    packages = build_package_info(user, data, package_detail_dict, documents_dict)

    if (request.body):
        return render(request, 'pages/check.html', {'packages': filter_packages(request, packages)})                         
    
    return render(request, 'pages/check.html', {'packages': packages})
