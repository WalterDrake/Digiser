from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
import re

def is_valid_package_id(package_id):
    return isinstance(package_id, str) and re.match(r'^[a-zA-Z0-9_-]+$', package_id)

class DataCrossValidator_Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.method == 'POST' and request.path.startswith('/document/'):
            pattern = r'^/document/([a-zA-Z0-9]{16})/(\d+)/?$'

            # Check if the request path matches the pattern
            match = re.match(pattern, request.path)
            if match:
                form_data = self.get_BCD_form_data(request)
                if form_data is None:
                    return HttpResponse("Invalid form", content_type="text/plain; charset=utf-8")
                
                self.data = form_data
                try:
                    error_list = self.process_request_BCD(request)
                    request.form_data = self.data
                    # Add error_list to request for further use
                    request.error_list = error_list
                except AssertionError as e:
                    return HttpResponse(f"Error: {str(e)}", content_type="text/plain; charset=utf-8")
    

        return self.get_response(request)
    
    def process_request_BCD(self, request):
        date_fields = ['ngayDangKy', 'nksNgaySinh', 'meNgaySinh', 'chaNgaySinh', 'nycNgayCapGiayToTuyThan']

        for field in date_fields:
            if self.data.get(field):
                if isinstance(self.data[field], str):
                    try:
                        self.data[field] = datetime.strptime(self.data[field], "%d/%m/%Y").date()
                    except (ValueError, TypeError):
                        self.data[field] = None
        
        chaNgaySinh = self.data.get('chaNgaySinh')
        meNgaySinh = self.data.get('meNgaySinh')
        ngayDangKy = self.data.get('ngayDangKy')
        nksNgaySinh = self.data.get('nksNgaySinh')
        nksQuocTich = self.data.get('nksQuocTich')
        nksDanToc = self.data.get('nksDanToc')
        chaSoGiayToTuyThan = self.data.get('chaSoGiayToTuyThan')
        nycSoGiayToTuyThan = self.data.get('nycSoGiayToTuyThan')
        meSoGiayToTuyThan = self.data.get('meSoGiayToTuyThan')
        chaNoiCuTru = self.data.get('chaNoiCuTru')
        meNoiCuTru = self.data.get('meNoiCuTru')
        chaLoaiCuTru = self.data.get('chaLoaiCuTru')
        meLoaiCuTru = self.data.get('meLoaiCuTru')
        meDanToc = self.data.get('meDanToc')
        meQuocTich = self.data.get('meQuocTich')
        chaDanToc = self.data.get('chaDanToc')
        chaQuocTich = self.data.get('chaQuocTich')
        nksLoaiKhaiSinh = self.data.get('nksLoaiKhaiSinh')
        nycHoTen = self.data.get('nycHoTen')
        nksHoTen = self.data.get('nksHoTen')
        nycNgayCapGiayToTuyThan = self.data.get('nycNgayCapGiayToTuyThan')
        
        # Initialize the error list
        error_list = []

        now = datetime.now()

        # Check age differences for father
        if chaNgaySinh is not None:
            diff_cha = now.year - chaNgaySinh.year - ((now.month, now.day) < (chaNgaySinh.month, chaNgaySinh.day))
            if diff_cha < 20:
                error_list.append("chaNgaySinh phải lớn hơn hoặc bằng 20 năm trước tính từ thời điểm hiện tại")
            if nksNgaySinh is not None and not chaNgaySinh < nksNgaySinh:
                error_list.append("chaNgaySinh phải trước nksNgaySinh")

        # Check age differences for mother
        if meNgaySinh is not None:
            diff_me = now.year - meNgaySinh.year - ((now.month, now.day) < (meNgaySinh.month, meNgaySinh.day))
            if diff_me < 18:
                error_list.append("meNgaySinh phải lớn hơn hoặc bằng 18 năm trước tính từ thời điểm hiện tại")
            if nksNgaySinh is not None and not meNgaySinh < nksNgaySinh:
                error_list.append("meNgaySinh phải trước nksNgaySinh")

        # Check nationality and ethnicity
        if nksQuocTich != "Việt Nam" and nksDanToc != 'Khác':
            error_list.append("nksDanToc không được thuộc Việt nam nếu nksQuocTich không phải Việt Nam")
        if chaQuocTich != "Việt Nam" and chaDanToc != 'Khác':
            error_list.append("chaDanToc không được thuộc Việt nam nếu chaQuocTich không phải Việt Nam")
        if meQuocTich != "Việt Nam" and meDanToc != 'Khác':
            error_list.append("meDanToc không được thuộc Việt nam nếu meQuocTich không phải Việt Nam")

        # Check ID numbers
        if chaSoGiayToTuyThan is not None and nycSoGiayToTuyThan is not None:
            if chaSoGiayToTuyThan == nycSoGiayToTuyThan:
                error_list.append("chaSoGiayToTuyThan và nycSoGiayToTuyThan không được trùng nhau")
        if chaSoGiayToTuyThan is not None and meSoGiayToTuyThan is not None:
            if chaSoGiayToTuyThan == meSoGiayToTuyThan:
                error_list.append("chaSoGiayToTuyThan và meSoGiayToTuyThan không được trùng nhau")
        if meSoGiayToTuyThan is not None and nycSoGiayToTuyThan is not None:
            if meSoGiayToTuyThan == nycSoGiayToTuyThan:
                error_list.append("meSoGiayToTuyThan và nycSoGiayToTuyThan không được trùng nhau")

        # Check residence information
        if chaNoiCuTru is None and chaLoaiCuTru != 0:
            error_list.append("chaLoaiCuTru phải thuộc trường không có thông tin khi chaNoiCuTru bỏ trống")
        if meNoiCuTru is None and meLoaiCuTru != 0:
            error_list.append("meLoaiCuTru phải thuộc trường không có thông tin khi meNoiCuTru bỏ trống")

        # Check identity determination
        me_variables = ['meSoGiayToTuyThan', 'meLoaiCuTru', 'meNoiCuTru', 'meNgaySinh', 'meQuocTich', 'meHoTen', 'meDanToc']
        cha_variables = ['chaSoGiayToTuyThan', 'chaLoaiCuTru', 'chaNoiCuTru', 'chaNgaySinh', 'chaQuocTich', 'chaHoTen', 'chaDanToc']

        if nksLoaiKhaiSinh == 'Chưa xác định được mẹ':
            identity_errors_me = self.validate_identity_not_determined(me_variables, 'me')
            error_list.extend(identity_errors_me)
        elif nksLoaiKhaiSinh == 'Chưa xác định được cha':
            identity_errors_cha = self.validate_identity_not_determined(cha_variables, 'cha')
            error_list.extend(identity_errors_cha)
        elif nksLoaiKhaiSinh == 'Chưa xác định được cả cha lẫn mẹ':
            identity_errors_me = self.validate_identity_not_determined(me_variables, 'me')
            identity_errors_cha = self.validate_identity_not_determined(cha_variables, 'cha')
            error_list.extend(identity_errors_me + identity_errors_cha)

        # Check name duplication
        if nycHoTen is not None and nksHoTen is not None:
            if nycHoTen == nksHoTen:
                error_list.append("nycHoTen và nksHoTen không được trùng nhau")

        # Check if ngayDangKy is not None
        if ngayDangKy is not None:
            def compare_dates(ngayDangKy, *dates):
                for date in dates:
                    if date is not None and not ngayDangKy > date:
                        return False
                return True
            
            if not compare_dates(ngayDangKy, meNgaySinh, chaNgaySinh, nksNgaySinh, nycNgayCapGiayToTuyThan):
                error_list.append("ngayDangKy phải lớn hơn tất cả các ngày trong form")
        return error_list

    def validate_identity_not_determined(self, variables_list, gender):
        """
        Validates that all variables in variables_list are None when gender's identity has not been determined.

        :param variables_list: List of variable names to check.
        :param gender: The gender whose identity has not been determined ('me' for mother, 'cha' for father).
        """

        error_list = []

        # Iterate through each variable in the list
        for var_name in variables_list:
            # Retrieve the variable value
            var_value = self.data.get(var_name)
            if var_value is not None:
                error_list.append(f"{var_name} không thể có giá trị khi danh tính người {gender} chưa được xác định.")
        return error_list

    def get_BCD_form_data(self, request):
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
            'nycNoiCapGiayToTuyThan': request.POST.get('nycNoiCapGiayToTuyThan')
        }
