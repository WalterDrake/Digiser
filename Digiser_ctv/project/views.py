from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.utils.html import escape
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
import re
from .models.model2 import Birth_Certificate_Document
from .models.model1 import Document, Package_detail, Package
from authentication.models import CustomUser
from django.forms.models import model_to_dict
from datetime import datetime, date
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .utils import birth_certificate_documents_to_sheet

@login_required
def input_redirect(request, **kwargs):
    user_code = request.session.get('user_code')
    user = get_object_or_404(CustomUser, code=user_code)

    package_id = kwargs.get('id')
    if not is_valid_package_id(package_id):
        raise Http404("Invalid package ID")

    package_id = escape(package_id)
    package_detail = get_object_or_404(Package_detail, package_name_hash=package_id)

    if user not in {package_detail.inserter, package_detail.checker_1, package_detail.checker_2}:
        raise Http404("Document does not exist")

    documents = Document.objects.filter(package_name=package_detail.package_name)

    index = get_valid_index(kwargs.get('index', 0), len(documents))

    document = documents[index]

    if document.type == "KS":
        if user == package_detail.inserter:
            return birth_certificate_document(request, document, user, role="inserter", package_detail_name=package_detail)
        elif user == package_detail.checker_1:
            return birth_certificate_document(request, document, user, role="checker_1")
        elif user == package_detail.checker_2:
            return birth_certificate_document(request, document, user, role="checker_2")
    else:
        raise Http404("Document type not supported")
    
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
@login_required
def export_package(request, **kwargs):
    package_id = kwargs.get('id')
    if not is_valid_package_id(package_id):
        raise Http404("Invalid package ID")

    package_id = escape(package_id)
    package = get_object_or_404(Package_detail, package_name_hash=package_id)

    documents = Document.objects.select_related('package_name').filter(package_name=package.package_name)

    birth_certificate_documents = Birth_Certificate_Document.objects.select_related('executor').prefetch_related('document').filter(document__in=documents)
    birth_certificate_documents_to_sheet(birth_certificate_documents)
        

def is_valid_package_id(package_id):
    return isinstance(package_id, str) and re.match(r'^[a-zA-Z0-9_-]+$', package_id)


def get_valid_index(index_str, documents_count):
    try:
        index = int(index_str)
        if 0 <= index < documents_count:
            return index
    except (ValueError, TypeError):
        pass
    raise Http404("Invalid document index")


def birth_certificate_document(request, document, user, role, package_detail_name=None):
    date_fields = ['ngayDangKy', 'nksNgaySinh', 'meNgaySinh', 'chaNgaySinh', 'nycNgayCapGiayToTuyThan']
    
    def prepare_form_data(form_instance, lock=False):
        if form_instance:
            document_name = form_instance.document.document_name.split('.')
            form_instance.so = document_name[4] if len(document_name) > 0 else ""
            form_instance.quyenSo = document_name[2] if len(document_name) > 0 else ""
            
            form_data = handle_date_fields(model_to_dict(form_instance), date_fields, rule="format")
            form_data.update({
                'pdf_path': form_instance.document.document_path,
                'lock': lock,
                'total_fields': form_instance.document.package_name.total_fields,
                'entered_tickets': form_instance.document.package_name.entered_tickets or 0,
                'total_real_tickets': form_instance.document.package_name.total_real_tickets
            })
            return form_data
        return {}

    if request.method == 'POST':
        form_data = get_form_data(request)
        if form_data is None:
            return render(request, 'pages/input.html', {'error': 'Invalid form.'})
        
        form_data = handle_date_fields(form_data, date_fields)
        form_data['executor'] = user
        form_instance, _ = Birth_Certificate_Document.objects.update_or_create(
            document=document, executor=user, defaults=form_data)
        if role == 'inserter':
            package = Package.objects.filter(package_name=package_detail_name).first()
            form_instance.document.package_name.entered_tickets = Birth_Certificate_Document.objects.filter(document__package_name=package, executor=user).count()
        form_data.update(get_form_data())
        form_data.update(prepare_form_data(form_instance))
        return render(request, 'pages/input.html', {'form': form_data})
    
    lock = False
    form_instance = None
    
    if role == 'inserter':
        form_instance = Birth_Certificate_Document.objects.filter(document=document).first()
        if form_instance and form_instance.document.status_insert == 'Đã nhập':
            lock = True
    else:
        form_instance = Birth_Certificate_Document.objects.filter(document=document, executor=user).first()
        if not form_instance and role == 'checker_2':
            form_instance = Birth_Certificate_Document.objects.filter(document=document, executor=user)[1:2].first()
        if not form_instance:
            form_instance = Birth_Certificate_Document.objects.filter(document=document).first()
        if form_instance and (form_instance.document.status_check_1 == 'Hoàn thành' or 
                              form_instance.document.status_check_2 == 'Hoàn thành'):
            lock = True
    
    form_data = get_form_data()
    form_data.update(prepare_form_data(form_instance, lock))
    
    template = 'pages/input.html' if role == 'inserter' else 'pages/check_birth.html'
    return render(request, template, {'form': form_data})


def get_form_data(request=None):
    if request is None:
        return {
            'DanToc': Birth_Certificate_Document._meta.get_field('nksDanToc').choices,
            'GioiTinh': Birth_Certificate_Document._meta.get_field('nksGioiTinh').choices,
            'QuocTich': Birth_Certificate_Document._meta.get_field('nksQuocTich').choices,
            'LoaiDangKy': Birth_Certificate_Document._meta.get_field('loaiDangKy').choices,
            'LoaiCuTru': Birth_Certificate_Document._meta.get_field('meLoaiCuTru').choices,
            'LoaiGiayToTuyThan': Birth_Certificate_Document._meta.get_field('meLoaiGiayToTuyThan').choices,
            'LoaiKhaiSinh': Birth_Certificate_Document._meta.get_field('nksLoaiKhaiSinh').choices,
            'pdf': Birth_Certificate_Document._meta.get_field('document')
        }

    try:
        return {
            'ngayDangKy': request.POST.get('ngayDangKy'),
            'nksNgaySinh': request.POST.get('nksNgaySinh'),
            'meNgaySinh': request.POST.get('meNgaySinh'),
            'chaNgaySinh': request.POST.get('chaNgaySinh'),
            'nycNgayCapGiayToTuyThan': request.POST.get('nycNgayCapGiayToTuyThan'),
            'so': request.POST.get('so'),
            'quyenSo': request.POST.get('quyenSo'),
            'trangSo': request.POST.get('trangSo'),
            'loaiDangKy': request.POST.get('loaiDangKy'),
            'noiDangKy': request.POST.get('noiDangKy'),
            'nguoiKy': request.POST.get('nguoiKy'),
            'chucVuNguoiKy': request.POST.get('chucVuNguoiKy'),
            'nguoiThucHien': request.POST.get('nguoiThucHien'),
            'ghiChu': request.POST.get('ghiChu'),
            'nksHoTen': request.POST.get('nksHoTen'),
            'nksGioiTinh': request.POST.get('nksGioiTinh'),
            'nksNgaySinhBangChu': request.POST.get('nksNgaySinhBangChu'),
            'nksNoiSinh': request.POST.get('nksNoiSinh'),
            'nksQueQuan': request.POST.get('nksQueQuan'),
            'nksDanToc': request.POST.get('nksDanToc'),
            'nksQuocTich': request.POST.get('nksQuocTich'),
            'nksLoaiKhaiSinh': request.POST.get('nksLoaiKhaiSinh'),
            'meHoTen': request.POST.get('meHoTen'),
            'meDanToc': request.POST.get('meDanToc'),
            'meQuocTich': request.POST.get('meQuocTich'),
            'meLoaiCuTru': request.POST.get('meLoaiCuTru'),
            'meNoiCuTru': request.POST.get('meNoiCuTru'),
            'meLoaiGiayToTuyThan': request.POST.get('meLoaiGiayToTuyThan'),
            'meSoGiayToTuyThan': request.POST.get('meSoGiayToTuyThan'),
            'chaHoTen': request.POST.get('chaHoTen'),
            'chaDanToc': request.POST.get('chaDanToc'),
            'chaQuocTich': request.POST.get('chaQuocTich'),
            'chaLoaiCuTru': request.POST.get('chaLoaiCuTru'),
            'chaNoiCuTru': request.POST.get('chaNoiCuTru'),
            'chaLoaiGiayToTuyThan': request.POST.get('chaLoaiGiayToTuyThan'),
            'chaSoGiayToTuyThan': request.POST.get('chaSoGiayToTuyThan'),
            'nycHoTen': request.POST.get('nycHoTen'),
            'nycQuanHe': request.POST.get('nycQuanHe'),
            'nycLoaiGiayToTuyThan': request.POST.get('nycLoaiGiayToTuyThan'),
            'nycGiayToKhac': request.POST.get('nycGiayToKhac'),
            'nycSoGiayToTuyThan': request.POST.get('nycSoGiayToTuyThan'),
            'nycNoiCapGiayToTuyThan': request.POST.get('nycNoiCapGiayToTuyThan'),
        }
    except (ValueError, TypeError):
        return None
    
def handle_date_fields(data, fields, rule="convert"):
    for field in fields:
        if field in data:
            if rule == "convert" and isinstance(data[field], str):
                try:
                    data[field] = datetime.strptime(data[field], "%d/%m/%Y").date()
                except (ValueError, TypeError):
                    data[field] = None
            elif rule == "format" and isinstance(data[field], date):
                data[field] = data[field].strftime('%d/%m/%Y')
    return data

# class DataCrossValidator:
#     def __init__(self, data):
#         """Constructor method."""
#         self.data = data

#     def validate_birth_cert_document(self):
#         # Cross validation fields
#         chaNgaySinh = self.data.get('chaNgaySinh')
#         meNgaySinh = self.data.get('meNgaySinh')
#         ngayDangKy = self.data.get('ngayDangKy')
#         nksNgaySinh = self.data.get('nksNgaySinh')
#         nksQuocTich = self.data.get('nksQuocTich')
#         nksDanToc = self.data.get('nksDanToc')
#         chaSoGiayToTuyThan = self.data.get('chaSoGiayToTuyThan')
#         nycSoGiayToTuyThan = self.data.get('nycSoGiayToTuyThan')
#         meSoGiayToTuyThan = self.data.get('meSoGiayToTuyThan')
#         chaNoiCuTru = self.data.get('chaNoiCuTru')
#         meNoiCuTru = self.data.get('meNoiCuTru')
#         chaLoaiCuTru = self.data.get('chaLoaiCuTru')
#         meLoaiCuTru = self.data.get('meLoaiCuTru')
#         meDanToc = self.data.get('meDanToc')
#         meQuocTich = self.data.get('meQuocTich')
#         chaDanToc = self.data.get('chaDanToc')
#         chaQuocTich = self.data.get('chaQuocTich')
#         nksLoaiKhaiSinh = self.data.get('nksLoaiKhaiSinh')
#         nycHoTen = self.data.get('nycHoTen')
#         nksHoTen = self.data.get('nksHoTen')
#         nycNgayCapGiayToTuyThan = self.data.get('nycNgayCapGiayToTuyThan')

#         # Calculate age differences
#         now = datetime.now()
#         diff_cha = now.year - chaNgaySinh.year - \
#             ((now.month, now.day) < (chaNgaySinh.month, chaNgaySinh.day))
#         diff_me = now.year - meNgaySinh.year - \
#             ((now.month, now.day) < (meNgaySinh.month, meNgaySinh.day))

#         # Check age conditions
#         assert diff_cha >= 20, "chaNgaySinh phải nhỏ hơn hoặc bằng 20 năm trước từ thời điểm hiện tại"
#         assert diff_me >= 18, "meNgaySinh phải nhỏ hơn hoặc bằng 18 năm trước từ thời điểm hiện tại"

#         # Check that both parents' birth dates are after the child's birth date
#         assert chaNgaySinh > nksNgaySinh, "chaNgaySinh phải sau nksNgaySinh"
#         assert meNgaySinh > nksNgaySinh, "meNgaySinh phải sau nksNgaySinh"

#         assert nksQuocTich != "Vietnam" and nksDanToc is None, "nksDanToc không được thuộc Việt nam nếu nksQuocTich không phải Việt Nam"
#         assert chaQuocTich != "Vietnam" and chaDanToc is None, "chaDanToc không được thuộc Việt nam nếu chaQuocTich không phải Việt Nam"
#         assert meQuocTich != "Vietnam" and meDanToc is None, "meDanToc không được thuộc Việt nam nếu meQuocTich không phải Việt Nam"

#         if chaSoGiayToTuyThan is not None and nycSoGiayToTuyThan is not None:
#             assert chaSoGiayToTuyThan != nycSoGiayToTuyThan, "chaSoGiayToTuyThan và nycSoGiayToTuyThan không được trùng nhau"
#         if chaSoGiayToTuyThan is not None and meSoGiayToTuyThan is not None:
#             assert chaSoGiayToTuyThan != nycSoGiayToTuyThan, "chaSoGiayToTuyThan và meSoGiayToTuyThan không được trùng nhau"
#         if meSoGiayToTuyThan is not None and nycSoGiayToTuyThan is not None:
#             assert chaSoGiayToTuyThan != nycSoGiayToTuyThan, "meSoGiayToTuyThan và nycSoGiayToTuyThan không được trùng nhau"

#         assert chaNoiCuTru is None and chaLoaiCuTru == 0, "chaLoaiCuTru phải thuộc trường không có thông tin khi chaNoiCuTru bỏ trống"
#         assert meNoiCuTru is None and meLoaiCuTru == 0, "meLoaiCuTru phải thuộc trường không có thông tin khi meNoiCuTru bỏ trống"

#         # Prepare a list of variables to check
#         me_variables = ['meSoGiayToTuyThan', 'meLoaiCuTru', 'meNoiCuTru',
#                         'meNgaySinh', 'meQuocTich', 'meHoTen', 'meDanToc']
#         cha_variables = ['chaSoGiayToTuyThan', 'chaLoaiCuTru', 'chaNoiCuTru',
#                          'chaNgaySinh', 'chaQuocTich', 'chaHoTen', 'chaDanToc']

#         # Check if nksLoaiKhaiSinh indicates mother's identity has not been determined
#         if nksLoaiKhaiSinh == 'Chưa xác định được mẹ':
#             self.validate_identity_not_determined(me_variables, 'me')
#         elif nksLoaiKhaiSinh == 'Chưa xác định được cha':
#             self.validate_identity_not_determined(cha_variables, 'cha')
#         elif nksLoaiKhaiSinh == 'Chưa xác định được cả cha lẫn mẹ':
#             self.validate_identity_not_determined(me_variables, 'me')
#             self.validate_identity_not_determined(cha_variables, 'cha')

#         assert nycHoTen != nksHoTen, "nycHoTen và nksHoTen không được trùng nhau"

#         assert (ngayDangKy > meNgaySinh and ngayDangKy > chaNgaySinh and ngayDangKy > nksNgaySinh and ngayDangKy >
#                 nycNgayCapGiayToTuyThan), "ngayDangKy phải lớn hơn tất cả các ngày trong form"

#     def validate_identity_not_determined(self, variables_list, gender):
#         """
#         Validates that all variables in variables_list are None when gender's identity has not been determined.

#         :param variables_list: List of variable names to check.
#         :param gender: The gender whose identity has not been determined ('me' for mother, 'cha' for father).
#         """

#         # Iterate through each variable in the list
#         for var_name in variables_list:
#             # Retrieve the variable value
#             var_value = self.data.get(var_name)

#             # Assert that the variable value is None (null)
#             assert var_value is None, f"{var_name} không thể có giá trị khi danh tính người {gender} chưa được xác định."