from django.shortcuts import render
from .models.model2 import Birth_Certificate_Document
from .models.model1 import Document, Package_detail
from datetime import datetime
# Create your views here.


def create_birth_certificate_document(request):
    document = Document.objects.filter(document_id=request.GET.get('id')).first()
    package = Package_detail.objects.filter(package_name_hash=request.GET.get('hash')).first()
    so =  ""
    quyenSo = ""
    trangSo = ""
    if request.method == 'POST':
        ngayDangKy = datetime.strptime(
            request.POST.get('ngayDangKy'), "%Y-%m-%d").date()
        nksNgaySinh = datetime.strptime(
            request.POST.get('nksNgaySinh'), "%Y-%m-%d").date()
        meNgaySinh = datetime.strptime(
            request.POST.get('meNgaySinh'), "%Y-%m-%d").date()
        chaNgaySinh = datetime.strptime(
            request.POST.get('chaNgaySinh'), "%Y-%m-%d").date()
        nycNgayCapGiayToTuyThan = datetime.strptime(
            request.POST.get('nycNgayCapGiayToTuyThan'), "%Y-%m-%d").date()
        form = {
            'document': document,
            'so': so,
            'quyenSo': quyenSo,
            'trangSo': trangSo,
            'ngayDangKy': ngayDangKy,
            'loaiDangKy': request.POST.get('loaiDangKy'),
            'noiDangKy': request.POST.get('noiDangKy'),
            'nguoiKy': request.POST.get('nguoiKy'),
            'chucVuNguoiKy': request.POST.get('chucVuNguoiKy'),
            'nguoiThucHien': request.POST.get('nguoiThucHien'),
            'ghiChu': request.POST.get('ghiChu'),
            'nksHoTen': request.POST.get('nksHoTen'),
            'nksGioiTinh': request.POST.get('nksGioiTinh'),
            'nksNgaySinh': nksNgaySinh,
            'nksNgaySinhBangChu': request.POST.get('nksNgaySinhBangChu'),
            'nksNoiSinh': request.POST.get('nksNoiSinh'),
            'nksQueQuan': request.POST.get('nksQueQuan'),
            'nksDanToc': request.POST.get('nksDanToc'),
            'nksQuocTich': request.POST.get('nksQuocTich'),
            'nksLoaiKhaiSinh': request.POST.get('nksLoaiKhaiSinh'),
            'meHoTen': request.POST.get('meHoTen'),
            'meNgaySinh': meNgaySinh,
            'meDanToc': request.POST.get('meDanToc'),
            'meQuocTich': request.POST.get('meQuocTich'),
            'meLoaiCuTru': request.POST.get('meLoaiCuTru'),
            'meNoiCuTru': request.POST.get('meNoiCuTru'),
            'meLoaiGiayToTuyThan': request.POST.get('meLoaiGiayToTuyThan'),
            'meSoGiayToTuyThan': request.POST.get('meSoGiayToTuyThan'),
            'chaHoTen': request.POST.get('chaHoTen'),
            'chaNgaySinh': chaNgaySinh,
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
            'nycNgayCapGiayToTuyThan': nycNgayCapGiayToTuyThan,
            'nycNoiCapGiayToTuyThan': request.POST.get('nycNoiCapGiayToTuyThan'),
        }

        birth_certificate_document = Birth_Certificate_Document(**form)
        birth_certificate_document.save()

        return render(request, 'input.html', {'form': form})
    else:
        form = Birth_Certificate_Document.objects.filter(document=document).first()
        if form is None:
            form = None
    return render(request, 'input.html', {'form': form})
