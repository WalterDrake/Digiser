from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from authentication.forms import CustomUserInfoChangeForm, CustomUserBankChangeForm
from django.db.models import Max, Sum, Q
from authentication.models import CustomUser, LoginLog
from .models import Salary
from project.models.model1 import Package_detail, Document
import json

@login_required
def home(request):
    if request.method == 'GET':
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

def handle_get_request(request):
    user_code = request.session.get('user_code')
    user = get_object_or_404(CustomUser, code=user_code)
    if checkManager(user):
        return redirect('home admin')  # Redirect to a URL pattern name for managers
    
    total_salary = statistic_salary(user)
    total_project_details = statistic_project(user)
    context = {
        'total_project_details' : total_project_details,
        'total_salary' : total_salary
    }
    return render(request, 'pages/dashboard.html', context)


@login_required
def insert(request):
    return render(request, 'pages/insert.html')


@login_required
def check(request):
    return render(request, 'pages/check.html')


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
def kh_input(request):
    return render(request, 'pages/kh_input.html')

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


def get_package_data(filter_user):
    data = Package_detail.objects.filter(filter_user).select_related('package_name')
    package_names = [s.package_name for s in data]

    package_details = Package_detail.objects.filter(package_name__in=package_names)
    documents = Document.objects.filter(package_name__in=package_names)
    package_detail_dict = {detail.package_name: detail for detail in package_details}
    documents_dict = {doc.package_name: [] for doc in documents}
    for doc in documents:
        documents_dict[doc.package_name].append(doc)
    return data, package_detail_dict, documents_dict

def build_package_info(user, data, package_detail_dict, documents_dict):
    packages = []
    for datum in data:
        package_name = datum.package_name
        package_detail = package_detail_dict.get(package_name)

        package_info = {
            'package': package_name.package_name,
            'total_tickets': package_name.total_tickets,
            'executor': user.full_name,
            'status_package': package_name.payment, 
            'received_day': None,
            'deadline_day': None,
            'datarecord_set': [],
        }
        if package_detail:
            if package_detail.inserter and user.full_name == package_detail.inserter.full_name:
                package_info['received_day'] = package_detail.start_insert.strftime('%d/%m/%Y')
                package_info['deadline_day'] = package_detail.finish_insert.strftime('%d/%m/%Y')
            elif package_detail.checker_1 and user.full_name == package_detail.checker_1.full_name or package_detail.checker_2 and user.full_name == package_detail.checker_2.full_name:
                package_info['received_day'] = package_detail.start_check.strftime('%d/%m/%Y')
                package_info['deadline_day'] = package_detail.finish_check.strftime('%d/%m/%Y')

        if package_detail:
            if package_detail.inserter and user.full_name == package_detail.inserter.full_name:
                package_info['received_day'] = package_detail.start_insert.strftime('%d/%m/%Y')
                package_info['deadline_day'] = package_detail.finish_insert.strftime('%d/%m/%Y')
            elif package_detail.checker_1 and user.full_name == package_detail.checker_1.full_name or package_detail.checker_2 and user.full_name == package_detail.checker_2.full_name:
                package_info['received_day'] = package_detail.start_check.strftime('%d/%m/%Y')
                package_info['deadline_day'] = package_detail.finish_check.strftime('%d/%m/%Y')

        related_documents = documents_dict.get(package_name, [])
        for document in related_documents:
            document_info = {
                'parent': package_name.package_name,
                'document_name': document.document_name,
                'fields': document.fields,
                'executor': None,
                'status': None,
                'errors': document.errors or 0,
                'type': document.type,
            }

            if package_detail:
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

    return packages

def filter_packages(request, packages):
    filters = json.loads(request.body)
    filtered_packages = []
    record_fields = ['status','type']
    package_filters = {}
    record_filters = {}
    package_matches = False
    filtered_datarecord_set = None

    record_filters = {key: value for key, value in filters.items() if key in record_fields}
    package_filters = {key: value for key, value in filters.items() if key not in record_fields}
    
    for package in packages:
        if len(record_filters) and len(package_filters):
            if len(package['datarecord_set']):
                package_matches = all(key in package and package.get(key) == value for key, value in package_filters.items())
                filtered_datarecord_set = [
                    record for record in package['datarecord_set']
                    if all(key in record and record.get(key) == value for key, value in record_filters.items())
                ]
                if package_matches and filtered_datarecord_set:
                    filtered_package = package.copy()
                    filtered_package['datarecord_set'] = filtered_datarecord_set
                    filtered_packages.append(filtered_package)

        elif len(package_filters) and len(package['datarecord_set']):
            package_matches = all(key in package and package.get(key) == value for key, value in package_filters.items())
            if package_matches:
                filtered_package = package.copy()
                filtered_packages.append(filtered_package)

        elif len(record_filters) and len(package['datarecord_set']):
            filtered_datarecord_set = [
                record for record in package['datarecord_set']
                if all(key in record and record.get(key) == value for key, value in record_filters.items())
            ]
            if filtered_datarecord_set:
                filtered_package = package.copy()
                filtered_package['datarecord_set'] = filtered_datarecord_set
                filtered_packages.append(filtered_package)

    return filtered_packages

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


def statistic_project(user):
    total_project_details = Salary.objects.filter(user=user).count()
    return total_project_details

def statistic_salary(user):
    total_salary = Salary.objects.filter(user=user).aggregate(Sum('final_salary'))['final_salary__sum']
    if total_salary is None:
        return 0
    return f"{total_salary:,}"


def statistic_users(request):
    limit = 200
    record = request.GET.get('record', limit)
    try:
        record = int(record)
        if record < 1:
            record = limit
    except ValueError:
        record = limit
    users_query = CustomUser.objects.all()[:record]
    return users_query

# def normalize_phone(phone_no):
#     phone = re.sub(r'\D', '', phone)

#     if len(phone_no) < 9:
#         raise ValueError("Phone number must be more than 9 digits")

#     return int(phone)

# def normalize_username(full_name):
#     normalized_name = unicodedata.normalize('NFKD', full_name).encode('ASCII', 'ignore').decode('ASCII')
#     normalized_name = normalized_name.lower()
#     normalized_name = re.sub(r'\s+', '', normalized_name)
#     normalized_name = re.sub(r'[^a-z0-9]', '', normalized_name)
#     return normalized_name


@login_required
@user_passes_test(checkManager)
def home_admin(request):
    return render(request, 'pages/home_admin.html')

@login_required
@user_passes_test(checkManager)
def ctv_list(request):
    users = CustomUser.objects.all()
    return render(request, 'pages/ctv_list.html', {
        'users': users,
        'status_choices': CustomUser._STATUSES,
        })
  
@login_required
@user_passes_test(checkManager)
def list_loginlog(request):
    loginlogs = LoginLog.objects.all()
    return render(request, 'pages/login_log.html', {'loginlogs': loginlogs})
