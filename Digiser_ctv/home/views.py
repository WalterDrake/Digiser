from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from authentication.forms import CustomUserInfoChangeForm, CustomUserBankChangeForm
from django.db.models import Max, Sum
from authentication.models import CustomUser
from .models import Salary
import re
from project.models.model1 import Package, Package_detail


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
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, username=user_id)
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
def input(request):
    return render(request, 'pages/input.html')

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
        project_name_trim = (datum.project_name.project_name).split("_")[0]
        project_name_trim = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', project_name_trim)
        package_name = datum.package_name.package_name

        if project_name_trim not in stats["Project"]:
            stats["Project"][project_name_trim] = {
                'packages': {},
                'total_votes': 0,
                'total_entered_votes': 0,
                'total_not_entered_votes': 0,
                'total_erroring_fields': 0,
            }

        if package_name not in stats["Project"][project_name_trim]['packages']:
            stats["Project"][project_name_trim]['packages'][package_name] = {
                'votes': 0,
                'entered_votes': 0,
                'not_entered_votes': 0,
                'erroring_fields': 0,
                'status': set()
            }
        package_info = Package.objects.get(project__project_name=datum.project_name.project_name, package_name=package_name)
        package_details_info = Package_detail.objects.get(package_name=package_name)
        stats["Project"][project_name_trim]['packages'][package_name]['votes'] += package_info.total_votes or 0
        stats["Project"][project_name_trim]['packages'][package_name]['entered_votes'] += package_info.entered_votes or 0
        stats["Project"][project_name_trim]['packages'][package_name]['not_entered_votes'] += package_info.not_entered_votes or 0
        stats["Project"][project_name_trim]['packages'][package_name]['erroring_fields'] += package_info.total_erroring_fields or 0
        stats["Project"][project_name_trim]['packages'][package_name]['status'].add(package_details_info.insert_status if datum.type == "Insert" else package_details_info.check_status )

        stats["Project"][project_name_trim]['total_votes'] += package_info.total_votes or 0
        stats["Project"][project_name_trim]['total_entered_votes'] += package_info.entered_votes or 0
        stats["Project"][project_name_trim]['total_not_entered_votes'] += package_info.not_entered_votes or 0
        stats["Project"][project_name_trim]['total_erroring_fields'] += package_info.total_erroring_fields or 0
        
    return stats


def statistic_Insert(user):
    return process_statistics(user, "Insert")


def statistic_Check(user):
    return process_statistics(user, "Check")


def show_data_statistic(request):
    data = data_statistics(request)
    print(data)
    projects = [
        {
            'name': 'DA050524_TKGoCong_KH2010_01',
            'tong_phieu': 80,
            'thuc_hien': 'Nguyễn Văn A',
            'trang_thai': 'Đã thanh toán',
            'ngay_nhan': '20/04/24',
            'deadline': '03/05/24',
            'datarecord_set': [
                {
                    'ten_du_lieu': 'Dữ liệu 01',
                    'tong_phieu': 10,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Văn A',
                    'trang_thai': 'Đã nhập',
                    'ngay_nhan': '20/04/24',
                    'deadline': '03/05/24',
                    'so_loi': 0,
                    'loai_file': 'KS',
                },
                {
                    'ten_du_lieu': 'Dữ liệu 02',
                    'tong_phieu': 10,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Văn A',
                    'trang_thai': 'Chưa check',
                    'ngay_nhan': '20/04/24',
                    'deadline': '03/05/24',
                    'so_loi': 0,
                    'loai_file': 'KS',
                },
                {
                    'ten_du_lieu': 'Dữ liệu 02',
                    'tong_phieu': 10,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Văn A',
                    'trang_thai': 'Chưa check',
                    'ngay_nhan': '20/04/24',
                    'deadline': '03/05/24',
                    'so_loi': 0,
                    'loai_file': 'KS',
                },
                {
                    'ten_du_lieu': 'Dữ liệu 03',
                    'tong_phieu': 10,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Văn A',
                    'trang_thai': 'Báo lỗi',
                    'ngay_nhan': '20/04/24',
                    'deadline': '03/05/24',
                    'so_loi': 2,
                    'loai_file': 'KH',
                },
                {
                    'ten_du_lieu': 'Dữ liệu 04',
                    'tong_phieu': 10,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Văn A',
                    'trang_thai': 'Nhập sai',
                    'ngay_nhan': '20/04/24',
                    'deadline': '03/05/24',
                    'so_loi': 1,
                    'loai_file': 'KH',
                },
                {
                    'ten_du_lieu': 'Dữ liệu 05',
                    'tong_phieu': 10,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Văn A',
                    'trang_thai': 'Chưa nhập',
                    'ngay_nhan': '20/04/24',
                    'deadline': '03/05/24',
                    'so_loi': 0,
                    'loai_file': 'HN',
                },
                {
                    'ten_du_lieu': 'Dữ liệu 06',
                    'tong_phieu': 10,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Văn A',
                    'trang_thai': 'Hoàn thành',
                    'ngay_nhan': '20/04/24',
                    'deadline': '03/05/24',
                    'so_loi': 0,
                    'loai_file': 'KS',
                },
                {
                    'ten_du_lieu': 'Dữ liệu 07',
                    'tong_phieu': 10,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Văn A',
                    'trang_thai': 'Hoàn thành',
                    'ngay_nhan': '20/04/24',
                    'deadline': '03/05/24',
                    'so_loi': 0,
                    'loai_file': 'KS',
                },
                {
                    'ten_du_lieu': 'Dữ liệu 08',
                    'tong_phieu': 10,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Văn A',
                    'trang_thai': 'Đã nhập',
                    'ngay_nhan': '20/04/24',
                    'deadline': '03/05/24',
                    'so_loi': 0,
                    'loai_file': 'KT',
                },
            ]
        },
        {
            'name': 'DA050524_TKGoCong_KH2010_01',
            'tong_phieu': 20,
            'thuc_hien': 'Trần Thanh B',
            'trang_thai': 'Đang thực hiện',
            'ngay_nhan': '25/04/24',
            'deadline': '15/05/24',
            'datarecord_set': [
                {
                    'ten_du_lieu': 'Dữ liệu 09',
                    'tong_phieu': 20,
                    'tong_truong': 18,
                    'thuc_hien': 'Trần Thanh B',
                    'trang_thai': 'Đang thực hiện',
                    'ngay_nhan': '25/04/24',
                    'deadline': '15/05/24',
                    'so_loi': 0,
                    'loai_file': 'KS',
                },
            ]
        },
        {
            'name': 'DA050524_TKGoCong_KH2010_01',
            'tong_phieu': 30,
            'thuc_hien': 'Nguyễn Hoàng C',
            'trang_thai': 'Đang thực hiện',
            'ngay_nhan': '30/04/24',
            'deadline': '20/05/24',
            'datarecord_set': [
                {
                    'ten_du_lieu': 'Dữ liệu 10',
                    'tong_phieu': 15,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Hoàng C',
                    'trang_thai': 'Chưa check',
                    'ngay_nhan': '30/04/24',
                    'deadline': '20/05/24',
                    'so_loi': 0,
                    'loai_file': 'CMC',
                },
                {
                    'ten_du_lieu': 'Dữ liệu 11',
                    'tong_phieu': 15,
                    'tong_truong': 18,
                    'thuc_hien': 'Nguyễn Hoàng C',
                    'trang_thai': 'Hoàn thành',
                    'ngay_nhan': '30/04/24',
                    'deadline': '20/05/24',
                    'so_loi': 0,
                    'loai_file': 'HN',
                },
            ]
        },
    ]
    context = {
        'projects': projects
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

