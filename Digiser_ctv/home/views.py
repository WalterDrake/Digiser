from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from Digiser_ctv.services import get_all_rows, add_row, count_row
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import UploadFileForm
from authentication.forms import CustomUserCreationForm, CustomUserChangeForm
import pandas as pd
import os
from authentication.models import CustomUser


@csrf_exempt
def upload_import(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            # Use openpyxl engine to read Excel file
            user_df = pd.read_excel(uploaded_file, engine='openpyxl')

            for _, user in user_df.iterrows():
                form = CustomUserCreationForm({"username": user['username'],
                                               "password1": user['password1'],
                                               "password2": user['password2'],
                                               "email": user['email'],
                                               "phone_no": user['phone_no']})

                doc_name = os.getenv("DOC_LIST").split(",")[0]
                if form.is_valid():
                    user = form.save(commit=False)
                    user.username = form.cleaned_data.get('email').split("@")[0]
                    user.save()  # Save the user instance
                    cnt = count_row(doc_name, 0)
                    user_dict = {
                        "ID": "",
                        "password": form.cleaned_data.get('password2'),
                        "gmail": user.email
                    }
                    add_row(doc_name, 0, cnt, user_dict)

            return JsonResponse({'message': 'File uploaded successfully'})
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def home(request):
    if request.method == 'POST':
        if (checkManager(request.user)):
            email = request.POST.get('gmail')
            doc_name = os.getenv("DOC_LIST").split(",")[0]
            cnt = count_row(doc_name, 0)
            user = get_object_or_404(CustomUser, email=email)
            user.is_verified = True
            user.role = 'CTV'
            user.code_ctv = 'NV' + str(cnt-1)
            user.save()
            return render(request, 'pages/home_manager.html')
    elif request.method == 'GET':
        doc_name = os.getenv("DOC_LIST").split(",")[0]
        raw_data = get_all_rows(doc_name, 1)
        num_rows = request.GET.get('rows', 10)
        try:
            num_rows = int(num_rows)
        except ValueError:
            num_rows = 10
        raw_data = raw_data[:num_rows]
        context = {
            'data': raw_data
        }
        user_id = request.session.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)

        if checkManager(user):
            return render(request, 'pages/home_manager.html', context)

        return render(request, 'pages/home_ctv.html', context)


def insert(request):
    return render(request, 'pages/insert.html')


def check(request):
    return render(request, 'pages/check.html')


def support(request):
    return render(request, 'pages/support.html')


def system(request):
    return render(request, 'pages/system.html')


def wiki(request):
    return render(request, 'pages/wiki.html')


def courses(request):
    return render(request, 'pages/courses.html')


def info(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            doc_name = os.getenv("DOC_LIST").split(",")[0]
            cnt = count_row(doc_name, 0)
            print(cnt)
            user_dict = {
                "ID" : user.code_ctv,
                "gmail": user.email,
                "password": user.password, # fixed hash password
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
            add_row(doc_name, 0, user.row, user_dict)
            context = {
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
            return render(request, 'pages/info.html', context)
    elif user.is_verified == True:
        user_id = request.session.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        context = {
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
        return render(request, 'pages/info.html', context)
    else:
        return render(request, 'pages/home_ctv.html')


def checkManager(user):
    if user.groups.filter(name='Manager').exists():
        return True
    return False
