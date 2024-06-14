from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Digiser_ctv.services import get_all_rows
import os
# Create your views here.
@login_required
def home(request):
    doc_name = os.getenv("DOC_LIST").split(",")[0]
    raw_data = get_all_rows(doc_name, 1)
    num_rows = request.GET.get('rows', 30)
    try:
        num_rows = int(num_rows)
    except ValueError:
        num_rows = 30
    raw_data = raw_data[:num_rows]
    context = {
        'data': raw_data
    }
    return render(request, 'pages/home.html', context )
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