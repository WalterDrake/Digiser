from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from authentication.forms import CustomUserInfoChangeForm, CustomUserBankChangeForm
from django.db.models import Max, Sum
from authentication.models import CustomUser
from .models import Salary
import re
from project.models.model1 import Package_detail, Document
import unicodedata
from django.utils.dateformat import format

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
    latest_ctv = CustomUser.objects.filter(role='EMPLOYEEE').aggregate(Max('code'))
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
        user.role = 'EMPLOYEE'
        latest_number = get_latest_ctv_number()
        user.code = generate_code("NV", latest_number)
        user.save()
    return render(request, 'pages/home_manager.html')


def handle_get_request(request):
    user_code = request.session.get('user_code')
    user = get_object_or_404(CustomUser, code=user_code)
    if checkManager(user):
        data = statistic_human(request)
        return render(request, 'pages/home_manager.html', {'users': data})
    
    total_salary = statistic_salary(user)
    total_project_details = statistic_project(user)
    context = {
        'total_project_details' : total_project_details,
        'total_salary' : total_salary
    }
    data = statistic_human(request)
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


def get_user_context(user):
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
    return user.groups.filter(name='ADMIN').exists()


def show_data_statistic(request):
    user_code = request.session.get('user_code')
    user = get_object_or_404(CustomUser, code=user_code)
    
    salary_data = Salary.objects.filter(user=user).select_related('package_name')
    package_names = [s.package_name for s in salary_data]
    
    package_details = Package_detail.objects.filter(package_name__in=package_names)
    documents = Document.objects.filter(package_name__in=package_names)

    package_detail_dict = {detail.package_name: detail for detail in package_details}
    documents_dict = {}
    for doc in documents:
        if doc.package_name not in documents_dict:
            documents_dict[doc.package_name] = []
        documents_dict[doc.package_name].append(doc)


    packages = []
    for datum in salary_data:
        package_name = datum.package_name
        package_detail = package_detail_dict.get(package_name)
        
        package_info = {
            'package': package_name.package_name,
            'total_tickets': package_name.total_tickets,
            'executor': user.full_name,
            'status': package_name.payment,
            'start_day': format(package_detail.start_insert, 'd/m/y') if package_detail and package_detail.start_insert else None,
            'finish_day': format(package_detail.finish_insert, 'd/m/y') if package_detail and package_detail.finish_insert else None,
            'datarecord_set': []
        }

        related_documents = documents_dict.get(package_name, [])
        for document in related_documents:
            document_info = {
                'document_path': document.document_path,
                'fields': document.fields,
                'executor' : None,
                'status' : None,
                'errors': document.errors,
                'type': document.type,
            }

            if package_detail.inserter and user.full_name == package_detail.inserter.full_name:
                document_info['executor'] = package_detail.inserter.full_name
                document_info['status'] = document.status_insert
            elif package_detail.checker_1 and user.full_name == package_detail.checker_1.full_name:
                document_info['executor'] = package_detail.checker_1.full_name
                document_info['status'] = document.status_check_1
            elif package_detail.checker_2 and user.full_name == package_detail.checker_2.full_name:
                document_info['executor'] = package_detail.checker_2.full_name
                document_info['status'] = document.status_check_2

            package_info['datarecord_set'].append(document_info)
        
        packages.append(package_info)

    context = {
        'packages': packages
    }
    return render(request, 'pages/statistic.html', context)



def statistic_project(user):
    total_project_details = Salary.objects.filter(user=user).count()
    return total_project_details

def statistic_salary(user):
    total_salary = Salary.objects.filter(user=user).aggregate(Sum('final_salary'))['final_salary__sum']
    total_salary = f"{total_salary:,}"
    return total_salary or 0


def statistic_human(request):
    record = request.GET.get('record', 10)
    try:
        record = int(record)
        if record < 1:
            record = 10
    except ValueError:
        record = 10
    users_query = CustomUser.objects.all()[:record]
    return users_query


def normalize_phone(phone_no):
    phone = re.sub(r'\D', '', phone)

    if len(phone_no) < 9:
        raise ValueError("Phone number must be more than 9 digits")

    return int(phone)

def normalize_username(full_name):
    normalized_name = unicodedata.normalize('NFKD', full_name).encode('ASCII', 'ignore').decode('ASCII')
    normalized_name = normalized_name.lower()
    normalized_name = re.sub(r'\s+', '', normalized_name)
    normalized_name = re.sub(r'[^a-z0-9]', '', normalized_name)

    return normalized_name
