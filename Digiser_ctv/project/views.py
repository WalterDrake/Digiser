from django.shortcuts import render, get_object_or_404
from .models.model2 import Birth_Certificate_Document
from .models.model1 import Document, Package_detail
from authentication.models import CustomUser
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def input_redirect(request):
    try:
        user_code = request.session.get('user_code')
        user = get_object_or_404(CustomUser, code=user_code)
        type = request.GET.get('type')
        if type == "KS":
            create_birth_certificate_document(request, user)
    except:
        return render('404.html')


@login_required
def create_birth_certificate_document(request, user):
    package = Package_detail.objects.filter(package_name_hash=request.GET.get('hash'), inserter=user).first()
    document = Document.objects.filter(document_id=request.GET.get('id')).first()
    if package and document:
        if request.method == 'POST':
            try:
                ngayDangKy = datetime.strptime(request.POST.get('ngayDangKy'), "%Y-%m-%d").date()
                nksNgaySinh = datetime.strptime(request.POST.get('nksNgaySinh'), "%Y-%m-%d").date()
                meNgaySinh = datetime.strptime(request.POST.get('meNgaySinh'), "%Y-%m-%d").date()
                chaNgaySinh = datetime.strptime(request.POST.get('chaNgaySinh'), "%Y-%m-%d").date()
                nycNgayCapGiayToTuyThan = datetime.strptime(request.POST.get('nycNgayCapGiayToTuyThan'), "%Y-%m-%d").date()
            except (ValueError, TypeError):
                return render(request, 'pages/input.html', {'error': 'Invalid date format.'})

            form_data = {
                'document': document,
                'so': request.POST.get('so', ''),
                'quyenSo': request.POST.get('quyenSo', ''),
                'trangSo': request.POST.get('trangSo', ''),
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

            birth_certificate_document = Birth_Certificate_Document(**form_data)
            birth_certificate_document.save()

            return render(request, 'pages/input.html', {'form': form_data})

        else:
            form_instance = Birth_Certificate_Document.objects.filter(document=document).first()
            form_data = {
                'DanToc': Birth_Certificate_Document._meta.get_field('nksDanToc').choices,
                'GioiTinh': Birth_Certificate_Document._meta.get_field('nksGioiTinh').choices,
                'QuocTich': Birth_Certificate_Document._meta.get_field('nksQuocTich').choices,
                'LoaiDangKy': Birth_Certificate_Document._meta.get_field('loaiDangKy').choices,
                'LoaiCuTru': Birth_Certificate_Document._meta.get_field('meLoaiCuTru').choices,
                'LoaiGiayToTuyThan': Birth_Certificate_Document._meta.get_field('meLoaiGiayToTuyThan').choices,
                'LoaiKhaiSinh': Birth_Certificate_Document._meta.get_field('nksLoaiKhaiSinh').choices,
            }

            if form_instance:
                form_data.update({
                    'document': form_instance.document,
                    'so': form_instance.so,
                    'quyenSo': form_instance.quyenSo,
                    'trangSo': form_instance.trangSo,
                    'ngayDangKy': form_instance.ngayDangKy,
                    'loaiDangKy': form_instance.loaiDangKy,
                    'noiDangKy': form_instance.noiDangKy,
                    'nguoiKy': form_instance.nguoiKy,
                    'chucVuNguoiKy': form_instance.chucVuNguoiKy,
                    'nguoiThucHien': form_instance.nguoiThucHien,
                    'ghiChu': form_instance.ghiChu,
                    'nksHoTen': form_instance.nksHoTen,
                    'nksGioiTinh': form_instance.nksGioiTinh,
                    'nksNgaySinh': form_instance.nksNgaySinh,
                    'nksNgaySinhBangChu': form_instance.nksNgaySinhBangChu,
                    'nksNoiSinh': form_instance.nksNoiSinh,
                    'nksQueQuan': form_instance.nksQueQuan,
                    'nksDanToc': form_instance.nksDanToc,
                    'nksQuocTich': form_instance.nksQuocTich,
                    'nksLoaiKhaiSinh': form_instance.nksLoaiKhaiSinh,
                    'meHoTen': form_instance.meHoTen,
                    'meNgaySinh': form_instance.meNgaySinh,
                    'meDanToc': form_instance.meDanToc,
                    'meQuocTich': form_instance.meQuocTich,
                    'meLoaiCuTru': form_instance.meLoaiCuTru,
                    'meNoiCuTru': form_instance.meNoiCuTru,
                    'meLoaiGiayToTuyThan': form_instance.meLoaiGiayToTuyThan,
                    'meSoGiayToTuyThan': form_instance.meSoGiayToTuyThan,
                    'chaHoTen': form_instance.chaHoTen,
                    'chaNgaySinh': form_instance.chaNgaySinh,
                    'chaDanToc': form_instance.chaDanToc,
                    'chaQuocTich': form_instance.chaQuocTich,
                    'chaLoaiCuTru': form_instance.chaLoaiCuTru,
                    'chaNoiCuTru': form_instance.chaNoiCuTru,
                    'chaLoaiGiayToTuyThan': form_instance.chaLoaiGiayToTuyThan,
                    'chaSoGiayToTuyThan': form_instance.chaSoGiayToTuyThan,
                    'nycHoTen': form_instance.nycHoTen,
                    'nycQuanHe': form_instance.nycQuanHe,
                    'nycLoaiGiayToTuyThan': form_instance.nycLoaiGiayToTuyThan,
                    'nycGiayToKhac': form_instance.nycGiayToKhac,
                    'nycSoGiayToTuyThan': form_instance.nycSoGiayToTuyThan,
                    'nycNgayCapGiayToTuyThan': form_instance.nycNgayCapGiayToTuyThan,
                    'nycNoiCapGiayToTuyThan': form_instance.nycNoiCapGiayToTuyThan,
                })

            return render(request, 'pages/input.html', {'form': form_data})
    else:
        return render('404.html')

