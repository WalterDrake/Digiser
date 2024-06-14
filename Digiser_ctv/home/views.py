from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Digiser_ctv.services import get_all_rows
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import UploadFileForm
from authentication.forms import CustomUserCreationForm
from Digiser_ctv.services import add_row, count_row
import pandas as pd
import os

# Create your views here.
@login_required
def home(request):
    return render(request, 'pages/home.html')

@csrf_exempt
def upload_import(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            user_df = pd.read_excel(uploaded_file, engine='openpyxl')  # Use openpyxl engine to read Excel file

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
                        "ID": "DGS" + str(cnt),
                        "password": form.cleaned_data.get('password2'),
                        "gmail": user.email
                    }
                    add_row(doc_name, 0, cnt, user_dict)
            
            return JsonResponse({'message': 'File uploaded successfully'})
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

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