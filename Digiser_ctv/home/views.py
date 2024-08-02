from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from authentication.forms import CustomUserInfoChangeForm, CustomUserBankChangeForm
from django.db.models import Max
from authentication.models import CustomUser
from django.contrib.auth.models import Group
from .models import Salary
import re
import os
from django.db.models import Sum

@login_required
def home(request):
    if request.method == 'POST':
        return handle_post_request(request)
    elif request.method == 'GET':
        return handle_get_request(request)

def generate_code(prefix, latest_number):
    new_number = latest_number + 1
    return f"{prefix}{new_number:04d}"

def get_latest_ctv_number():
    latest_ctv = CustomUser.objects.filter(role='CTV').aggregate(Max('code'))
    latest_code = latest_ctv['code__max']
    if latest_code:
        latest_number = int(latest_code.replace("NV", ""))
    else:
        latest_number = 0
    return latest_number

def handle_post_request(request):
    if checkManager(request.user):
        email = request.POST.get('gmail')
        user = get_object_or_404(CustomUser, email=email)
        user.is_verified = True
        user.role = 'CTV'
        latest_number = get_latest_ctv_number()
        user.code = generate_code("NV", latest_number)
        user.save()
    return render(request, 'pages/home_manager.html')


def handle_get_request(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, username=user_id)
    total_salary = statistic_salary(user)
    total_project_details = statistic_project(user)

    context = {
        'total_project_details' : total_project_details,
        'total_salary' : total_salary
    }
    if checkManager(user):
        data = statistic_human()
        return render(request, 'pages/home_manager.html', context)
    return render(request, 'pages/dashboard.html', context)


@login_required
def insert(request):
    return render(request, 'pages/insert.html')


@login_required
def check(request):
    return render(request, 'pages/check.html')


@login_required
def support(request):
    return render(request, 'pages/support.html')


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
def dashboard(request):
    return render(request, 'pages/dashboard.html')


@login_required
def info(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, username=user_id)
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
        print(form.cleaned_data)
        user = form.save(commit=False)
        user.save()
        return render(request, 'pages/info.html', get_user_context(user))
    return render(request, 'pages/info.html', get_user_context(user))


def handle_info_get(request, user):
    return render(request, 'pages/info.html', get_user_context(user))


def get_user_context(user):
    print(user)
    return {
        "code": user.code,
        "phone_no": user.phone_no,
        "birthday": user.birthday,
        "full_name": user.full_name,
        "address": user.address,
        "qualification": user.qualification,
        "identification": user.identification,
        "identification_address": user.identification_address,
        "note": user.note,
        "account_number": user.account_number,
        "bank_name": user.bank_name,
        "branch": user.branch,
        "owner": user.owner,
        "code_bank": user.code_bank
    }


def checkManager(user):
    return user.groups.filter(name='Manager').exists()


def data_statistics(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, username=user_id)
    statistics = {
        "Nhap": {},
        "Check": {},
    }
    statistics["Nhap"] = statistic_Insert(user)
    statistics["Check"] = statistic_Check(user)
    return statistics

def process_statistics(user, key):
    data = Salary.objects.filter(user=user,type=key)
    stats = {"Project": {}}
    for datum in data:
        project_name = (datum.project_name.project_name).split("_")[0]
        project_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', project_name)
        package_name = datum.package_name.package_name

        if project_name not in stats["Project"]:
            stats["Project"][project_name] = {
                'packages': {},
                'total_votes': 0,
                'total_acceptances': 0,
                'total_rejections': 0,
                'total_erroring_fields': 0,
            }

        if package_name not in stats["Project"][project_name]['packages']:
            stats["Project"][project_name]['packages'][package_name] = {
                'votes': 0,
                'acceptances': 0,
                'rejections': 0,
                'erroring_fields': 0,
                'status': set()
            }

        stats["Project"][project_name]['packages'][package_name]['votes'] += datum.total_votes or 0
        stats["Project"][project_name]['packages'][package_name]['acceptances'] += datum.total_fields or 0
        stats["Project"][project_name]['packages'][package_name]['rejections'] += datum.total_merging_votes or 0
        stats["Project"][project_name]['packages'][package_name]['erroring_fields'] += datum.total_erroring_fields or 0
        stats["Project"][project_name]['packages'][package_name]['status'].add(datum.status.insert_status if datum.type == "I" else datum.status.check_status )

        stats["Project"][project_name]['total_votes'] += datum.total_votes or 0
        stats["Project"][project_name]['total_acceptances'] += datum.total_fields or 0
        stats["Project"][project_name]['total_rejections'] += datum.total_merging_votes or 0
        stats["Project"][project_name]['total_erroring_fields'] += datum.total_erroring_fields or 0
        
    return stats


def statistic_Insert(user):
    return process_statistics(user, "I")


def statistic_Check(user):
    return process_statistics(user, "C")


def show_data_statistic(request):
    data = data_statistics(request)
    context = {'data': data}
    return render(request, 'pages/data_statistic.html', context)


def statistic_project(user):
    total_project_details = Salary.objects.filter(user=user).count()
    return total_project_details

def statistic_salary(user):
    total_salary = Salary.objects.filter(user=user).aggregate(Sum('final_salary'))['final_salary__sum']
    return total_salary or 0


def statistic_human():
    group_id = Group.objects.get(name='CTV')
    users = CustomUser.objects.filter(groups=group_id)
    user_dict = {}

    for user in users:
        if user.email not in user_dict:
            user_dict[user.email] = []
        user_dict[user.email].extend([user.code, user.role, user.is_verified, user.note])

    user_list = [{email: attributes} for email, attributes in user_dict.items()]
    return user_list
