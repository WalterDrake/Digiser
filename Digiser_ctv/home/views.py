from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from Digiser_ctv.services import get_all_rows, update_row, count_row
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import UploadFileForm
from authentication.forms import CustomUserCreationForm, CustomUserChangeForm
import pandas as pd
import os
from authentication.models import CustomUser

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
            "ID": "",
            "password": form.cleaned_data.get('password2'),
            "gmail": user.email
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
        user.code_ctv = f'NV{cnt-1}'
        user.save()
    return render(request, 'pages/home_manager.html')

def handle_get_request(request):
    doc_name = os.getenv("DOC_LIST").split(",")[0]
    raw_data = get_all_rows(doc_name, 1)
    num_rows = int(request.GET.get('rows', 10))
    context = {'data': raw_data[:num_rows]}
    
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)
    
    if checkManager(user):
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
def info(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        return handle_info_post(request, user)
    elif user.is_verified:
        return handle_info_get(request, user)
    else:
        handle_get_request()

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