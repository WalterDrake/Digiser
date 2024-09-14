from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

class DataCrossValidator_Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            form_data = self.get_BCD_form_data(request)
            if form_data is None:
                return HttpResponse("Invalid form", content_type="text/plain; charset=utf-8")
            
            self.data = form_data

            try:
                self.process_request_BCD(request)
                request.passMidleWare = self.data
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
        
        # Calculate age differences
    #     now = datetime.now()
    #     diff_cha = now.year - chaNgaySinh.year - \
    #         ((now.month, now.day) < (chaNgaySinh.month, chaNgaySinh.day))
    #     diff_me = now.year - meNgaySinh.year - \
    #         ((now.month, now.day) < (meNgaySinh.month, meNgaySinh.day))

    #     # Check age conditions
    #     assert diff_cha >= 20, "chaNgaySinh phải nhỏ hơn hoặc bằng 20 năm trước từ thời điểm hiện tại"
    #     assert diff_me >= 18, "meNgaySinh phải nhỏ hơn hoặc bằng 18 năm trước từ thời điểm hiện tại"

    #     # Check that both parents' birth dates are after the child's birth date
    #     assert chaNgaySinh > nksNgaySinh, "chaNgaySinh phải sau nksNgaySinh"
    #     assert meNgaySinh > nksNgaySinh, "meNgaySinh phải sau nksNgaySinh"
        
    #     # assert not (nksQuocTich != "Việt Nam" and nksDanToc == 'Khác'), "nksDanToc không được thuộc Việt nam nếu nksQuocTich không phải Việt Nam"
    #     # assert chaQuocTich != "Việt Nam" and chaDanToc == 'Khác', "chaDanToc không được thuộc Việt nam nếu chaQuocTich không phải Việt Nam"
    #     # assert meQuocTich != "Việt Nam" and meDanToc == 'Khác', "meDanToc không được thuộc Việt nam nếu meQuocTich không phải Việt Nam"

    #     if chaSoGiayToTuyThan is not None and nycSoGiayToTuyThan is not None:
    #         assert chaSoGiayToTuyThan != nycSoGiayToTuyThan, "chaSoGiayToTuyThan và nycSoGiayToTuyThan không được trùng nhau"
    #     if chaSoGiayToTuyThan is not None and meSoGiayToTuyThan is not None:
    #         assert chaSoGiayToTuyThan != nycSoGiayToTuyThan, "chaSoGiayToTuyThan và meSoGiayToTuyThan không được trùng nhau"
    #     if meSoGiayToTuyThan is not None and nycSoGiayToTuyThan is not None:
    #         assert chaSoGiayToTuyThan != nycSoGiayToTuyThan, "meSoGiayToTuyThan và nycSoGiayToTuyThan không được trùng nhau"

    #     assert chaNoiCuTru is None and chaLoaiCuTru == 0, "chaLoaiCuTru phải thuộc trường không có thông tin khi chaNoiCuTru bỏ trống"
    #     assert meNoiCuTru is None and meLoaiCuTru == 0, "meLoaiCuTru phải thuộc trường không có thông tin khi meNoiCuTru bỏ trống"

    #     # Prepare a list of variables to check
    #     me_variables = ['meSoGiayToTuyThan', 'meLoaiCuTru', 'meNoiCuTru',
    #                     'meNgaySinh', 'meQuocTich', 'meHoTen', 'meDanToc']
    #     cha_variables = ['chaSoGiayToTuyThan', 'chaLoaiCuTru', 'chaNoiCuTru',
    #                      'chaNgaySinh', 'chaQuocTich', 'chaHoTen', 'chaDanToc']

    #     # Check if nksLoaiKhaiSinh indicates mother's identity has not been determined
    #     if nksLoaiKhaiSinh == 'Chưa xác định được mẹ':
    #         self.validate_identity_not_determined(me_variables, 'me')
    #     elif nksLoaiKhaiSinh == 'Chưa xác định được cha':
    #         self.validate_identity_not_determined(cha_variables, 'cha')
    #     elif nksLoaiKhaiSinh == 'Chưa xác định được cả cha lẫn mẹ':
    #         self.validate_identity_not_determined(me_variables, 'me')
    #         self.validate_identity_not_determined(cha_variables, 'cha')

    #     assert nycHoTen != nksHoTen, "nycHoTen và nksHoTen không được trùng nhau"

    #     assert (ngayDangKy > meNgaySinh and ngayDangKy > chaNgaySinh and ngayDangKy > nksNgaySinh and ngayDangKy >
    #             nycNgayCapGiayToTuyThan), "ngayDangKy phải lớn hơn tất cả các ngày trong form"

    # def validate_identity_not_determined(self, variables_list, gender):
    #     """
    #     Validates that all variables in variables_list are None when gender's identity has not been determined.

    #     :param variables_list: List of variable names to check.
    #     :param gender: The gender whose identity has not been determined ('me' for mother, 'cha' for father).
    #     """

    #     # Iterate through each variable in the list
    #     for var_name in variables_list:
    #         # Retrieve the variable value
    #         var_value = self.data.get(var_name)

    #         # Assert that the variable value is None (null)
    #         assert var_value is None, f"{var_name} không thể có giá trị khi danh tính người {gender} chưa được xác định."

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
