from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Digiser_ctv.services import get_all_rows, update_row, count_row
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import UploadFileForm
from authentication.forms import CustomUserCreationForm, CustomUserChangeForm
import pandas as pd
import os
from authentication.models import CustomUser
from django.contrib.auth.models import Group


@csrf_exempt
def upload_import(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({'error': 'Form is not valid'}, status=400)

    user_df = pd.read_excel(request.FILES['file'], engine='openpyxl')
    doc_name = os.getenv("DOC_LIST").split(",")[0]

    for _, user in user_df.iterrows():
        process_user(user, doc_name)

    return JsonResponse({'message': 'File uploaded successfully'})


def process_user(user_data, doc_name):
    form = CustomUserCreationForm({
        "username": user_data['username'],
        "password1": user_data['password1'],
        "password2": user_data['password2'],
        "email": user_data['email'],
        "phone_no": user_data['phone_no']
    })

    if form.is_valid():
        user = form.save(commit=False)
        user.username = form.cleaned_data.get('email').split("@")[0]
        user.save()

        cnt = count_row(doc_name, 0)
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
        update_row(doc_name, 0, cnt, user_dict)


@login_required
def home(request):
    if request.method == 'POST':
        return handle_post_request(request)
    elif request.method == 'GET':
        return handle_get_request(request)


def handle_post_request(request):
    if checkManager(request.user):
        email = request.POST.get('gmail')
        doc_name = os.getenv("DOC_LIST").split(",")[0]
        cnt = count_row(doc_name, 0)
        user = get_object_or_404(CustomUser, email=email)
        user.is_verified = True
        user.role = 'CTV'
        print(cnt)
        user.code_ctv = generate_code("NV0000", user.row)
        user.save()
        update_user_info(user)
    return render(request, 'pages/home_manager.html')


def generate_code(base_str, number):
    number_str = str(number)
    base_length = len(base_str) - len(number_str)
    result = base_str[:base_length] + number_str
    return result


def handle_get_request(request):

    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)

    doc_name = os.getenv("DOC_LIST").split(",")[0]

    total_salary = statistic_salary(doc_name, user)
    total_project_details = statistic_project(doc_name, user)

    context = {
        'total_project_details' : total_project_details,
        'total_salary' : total_salary
    }
    if checkManager(user):
        data = statistic_human()
        print(data)
        return render(request, 'pages/home_manager.html', context)
    return render(request, 'pages/home_ctv.html', context)


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
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        return handle_info_post(request, user)
    elif user.is_verified:
        return handle_info_get(request, user)
    else:
        # handle_get_request()
        return redirect('/home')


def handle_info_post(request, user):
    form = CustomUserChangeForm(request.POST, instance=request.user)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        update_user_info(user)
        return render(request, 'pages/info.html', get_user_context(user))
    return render(request, 'pages/info.html')


def handle_info_get(request, user):
    return render(request, 'pages/info.html', get_user_context(user))


def update_user_info(user):
    doc_name = os.getenv("DOC_LIST").split(",")[0]
    user_dict = {
        "ID": user.code_ctv,
        "gmail": user.email,
        "password": user.password,
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


def get_user_context(user):
    return {
        "code_ctv": user.code_ctv,
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
    doc_name = os.getenv("DOC_LIST").split(",")[0]
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)
    statistics = {
        "Nhap": {},
        "Check": {},
    }
    statistics["Nhap"] = statistic_Nhap(doc_name, user)[0]
    statistics["Check"] = statistic_Check(doc_name, user)[0]
    return statistics

def process_statistics(raw_data, user_code_ctv, id_key):
    statistics = {"Du_An": {}}
    total_salary = 0
    total_project_details = 0

    for row in raw_data:
        if row[id_key].split("_")[0] == user_code_ctv:
            project = row["DuAn"].split("_")[0]
            project_package = row["magoiCV"]
            votes = row["Số phiếu"]
            status = row["Trạng thái nhập"]
            salary = row['Thành tiền']

            if project not in statistics["Du_An"]:
                statistics["Du_An"][project] = {
                    "magoiCV": {},
                    "total_votes": 0,
                    "total_acceptances": 0,
                    "total_rejections": 0,
                    "total_error": 0
                }

            if project_package not in statistics["Du_An"][project]["magoiCV"]:
                statistics["Du_An"][project]["magoiCV"][project_package] = {
                    "votes": set(),
                    "status": set(),
                    "acceptances": set(),
                    "rejections": set(),
                    "errors": set()
                }
                total_project_details += 1

            statistics["Du_An"][project]["magoiCV"][project_package]["votes"].add(votes)
            statistics["Du_An"][project]["magoiCV"][project_package]["status"].add(status)
            statistics["Du_An"][project]["magoiCV"][project_package]["acceptances"].add(0)
            statistics["Du_An"][project]["magoiCV"][project_package]["rejections"].add(0)
            statistics["Du_An"][project]["magoiCV"][project_package]["errors"].add(0)

            votes_value = int(votes) if votes else 0
            salary_value = int(salary) if salary else 0

            statistics["Du_An"][project]["total_votes"] += votes_value
            total_salary += salary_value

    for project in statistics["Du_An"]:
        for project_package in statistics["Du_An"][project]["magoiCV"]:
            for key in ["votes", "status", "acceptances", "rejections", "errors"]:
                statistics["Du_An"][project]["magoiCV"][project_package][key] = list(
                    statistics["Du_An"][project]["magoiCV"][project_package][key])

    return statistics, total_project_details, total_salary

def statistic_Nhap(doc_name, user):
    raw_data = get_all_rows(doc_name, 2)
    return process_statistics(raw_data, user.code_ctv, "ID CTV nhập")


def statistic_Check(doc_name, user):
    raw_data = get_all_rows(doc_name, 3)
    return process_statistics(raw_data, user.code_ctv, "ID CTV check")


def show_data_statistic(request):
    data = data_statistics(request)
    context = {
        'data': data
    }
    return render(request, 'pages/data_statistic.html', context)


def statistic_project(doc_name,user):
    total_project_details = statistic_Nhap(doc_name, user)[1] + statistic_Check(doc_name,user)[1]
    return total_project_details


def statistic_salary(doc_name, user):
    total_salary = statistic_Nhap(doc_name,user)[2] + statistic_Check(doc_name, user)[2]
    return total_salary


def statistic_human():
    group_id = Group.objects.get(name='CTV')
    users = CustomUser.objects.filter(groups=group_id)
    user_dict = {}

    for user in users:
        if user.email not in user_dict:
            user_dict[user.email] = []
        user_dict[user.email].extend([user.code_ctv, user.role, user.is_verified, user.note])

    user_list = [{email: attributes} for email, attributes in user_dict.items()]
    return user_list
