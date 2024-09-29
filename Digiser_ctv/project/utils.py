import pandas as pd
from .models.model2 import Birth_Certificate_Document
from typing import List
from datetime import date
import re
from django.forms.models import model_to_dict
from django.db.models.fields import Field

def birth_certificate_documents_to_df(birth_cert_docs: List[Birth_Certificate_Document]):
    data = []

    for birth_cert_doc in birth_cert_docs:
        data.append({
            'so': birth_cert_doc.so,
            'quyenSo': birth_cert_doc.quyenSo,
            'trangSo': birth_cert_doc.trangSo,
            'ngayDangKy': str(birth_cert_doc.ngayDangKy) if birth_cert_doc.ngayDangKy else None,
            'loaiDangKy': birth_cert_doc.loaiDangKy,
            'noiDangKy': birth_cert_doc.noiDangKy,
            'nguoiKy': birth_cert_doc.nguoiKy,
            'chucVuNguoiKy': birth_cert_doc.chucVuNguoiKy,
            'nguoiThucHien': birth_cert_doc.nguoiThucHien,
            'ghiChu': birth_cert_doc.ghiChu,
            'nksHoTen': birth_cert_doc.nksHoTen,
            'nksGioiTinh': birth_cert_doc.nksGioiTinh,
            'nksNgaySinh': str(birth_cert_doc.nksNgaySinh) if birth_cert_doc.nksNgaySinh else None,
            'nksNgaySinhBangChu': birth_cert_doc.nksNgaySinhBangChu,
            'nksNoiSinh': birth_cert_doc.nksNoiSinh,
            'nksNoiSinhDVHC': birth_cert_doc.nksNoiSinhDVHC,
            'nksQueQuan': birth_cert_doc.nksQueQuan,
            'nksDanToc': birth_cert_doc.nksDanToc,
            'nksQuocTich': birth_cert_doc.nksQuocTich,
            'nksQuocTichKhac': birth_cert_doc.nksQuocTichKhac,
            'nksLoaiKhaiSinh': birth_cert_doc.nksLoaiKhaiSinh,
            'nksMatTich': birth_cert_doc.nksMatTich,
            'nksMatTichNgayGhiChuTuyenBo': str(birth_cert_doc.nksMatTichNgayGhiChuTuyenBo) if birth_cert_doc.nksMatTichNgayGhiChuTuyenBo else None,
            'nksMatTichCanCuTuyenBo': birth_cert_doc.nksMatTichCanCuTuyenBo,
            'nksMatTichNgayGhiChuHuyTuyenBo': str(birth_cert_doc.nksMatTichNgayGhiChuHuyTuyenBo) if birth_cert_doc.nksMatTichNgayGhiChuHuyTuyenBo else None,
            'nksMatTichCanCuHuyTuyenBo': birth_cert_doc.nksMatTichCanCuHuyTuyenBo,
            'nksHanCheNangLucHanhVi': birth_cert_doc.nksHanCheNangLucHanhVi,
            'nksHanCheNangLucHanhViNgayGhiChuTuyenBo': str(birth_cert_doc.nksHanCheNangLucHanhViNgayGhiChuTuyenBo) if birth_cert_doc.nksHanCheNangLucHanhViNgayGhiChuTuyenBo else None,
            'nksHanCheNangLucHanhViCanCuTuyenBo': birth_cert_doc.nksHanCheNangLucHanhViCanCuTuyenBo,
            'nksHanCheNangLucHanhViNgayGhiChuHuyTuyenBo': str(birth_cert_doc.nksHanCheNangLucHanhViNgayGhiChuHuyTuyenBo) if birth_cert_doc.nksHanCheNangLucHanhViNgayGhiChuHuyTuyenBo else None,
            'nksHanCheNangLucHanhViNgayCanCuHuyTuyenBo': birth_cert_doc.nksHanCheNangLucHanhViNgayCanCuHuyTuyenBo,
            'meHoTen': birth_cert_doc.meHoTen,
            'meNgaySinh': str(birth_cert_doc.meNgaySinh) if birth_cert_doc.meNgaySinh else None,
            'meDanToc': birth_cert_doc.meDanToc,
            'meQuocTich': birth_cert_doc.meQuocTich,
            'meQuocTichKhac': birth_cert_doc.meQuocTichKhac,
            'meLoaiCuTru': birth_cert_doc.meLoaiCuTru,
            'meNoiCuTru': birth_cert_doc.meNoiCuTru,
            'meLoaiGiayToTuyThan': birth_cert_doc.meLoaiGiayToTuyThan,
            'meSoGiayToTuyThan': birth_cert_doc.meSoGiayToTuyThan,
            'chaHoTen': birth_cert_doc.chaHoTen,
            'chaNgaySinh': str(birth_cert_doc.chaNgaySinh) if birth_cert_doc.chaNgaySinh else None,
            'chaDanToc': birth_cert_doc.chaDanToc,
            'chaQuocTich': birth_cert_doc.chaQuocTich,
            'chaQuocTichKhac': birth_cert_doc.chaQuocTichKhac,
            'chaLoaiCuTru': birth_cert_doc.chaLoaiCuTru,
            'chaNoiCuTru': birth_cert_doc.chaNoiCuTru,
            'chaLoaiGiayToTuyThan': birth_cert_doc.chaLoaiGiayToTuyThan,
            'chaSoGiayToTuyThan': birth_cert_doc.chaSoGiayToTuyThan,
            'nycHoTen': birth_cert_doc.nycHoTen,
            'nycQuanHe': birth_cert_doc.nycQuanHe,
            'nycLoaiGiayToTuyThan': birth_cert_doc.nycLoaiGiayToTuyThan,
            'nycGiayToKhac': birth_cert_doc.nycGiayToKhac,
            'nycSoGiayToTuyThan': birth_cert_doc.nycSoGiayToTuyThan,
            'nycNgayCapGiayToTuyThan': str(birth_cert_doc.nycNgayCapGiayToTuyThan) if birth_cert_doc.nycNgayCapGiayToTuyThan else None,
            'nycNoiCapGiayToTuyThan': birth_cert_doc.nycNoiCapGiayToTuyThan,
            'soDangKyNuocNgoai': birth_cert_doc.soDangKyNuocNgoai,
            'ngayDangKyNuocNgoai': str(birth_cert_doc.ngayDangKyNuocNgoai) if birth_cert_doc.ngayDangKyNuocNgoai else None,
            'cqNuocNgoaiDaDangKy': birth_cert_doc.cqNuocNgoaiDaDangKy,
            'qgNuocNgoaiDaDangKy': birth_cert_doc.qgNuocNgoaiDaDangKy,
        })

    df = pd.DataFrame(data)
    return df


def get_form_data_choices():
        return {
            'DanToc': Birth_Certificate_Document._meta.get_field('nksDanToc').choices,
            'GioiTinh': Birth_Certificate_Document._meta.get_field('nksGioiTinh').choices,
            'QuocTich': Birth_Certificate_Document._meta.get_field('nksQuocTich').choices,
            'LoaiDangKy': Birth_Certificate_Document._meta.get_field('loaiDangKy').choices,
            'LoaiCuTru': Birth_Certificate_Document._meta.get_field('meLoaiCuTru').choices,
            'LoaiGiayToTuyThan': Birth_Certificate_Document._meta.get_field('meLoaiGiayToTuyThan').choices,
            'LoaiKhaiSinh': Birth_Certificate_Document._meta.get_field('nksLoaiKhaiSinh').choices,
        }


def handle_date_fields(data, fields):
    for field in fields:
        if field in data:
            if isinstance(data[field], date):
                data[field] = data[field].strftime('%d/%m/%Y')
    return data


def is_superuser(user):
    return user.is_superuser


def is_valid_package_id(package_id):
    return isinstance(package_id, str) and re.match(r'^[a-zA-Z0-9_-]+$', package_id)


def prepare_form_data(document, form_instance=None, lock=False, date_fields=None):
    document_name = form_instance.document.document_name.split('.') if form_instance else document.document_name.split('.')
    common_data = {
        'pdf_path': form_instance.document.document_path if form_instance else document.document_path,
        'lock': lock,
        'total_fields': form_instance.document.package_name.total_fields if form_instance else document.package_name.total_fields,
        'entered_tickets': form_instance.document.package_name.entered_tickets if form_instance else document.package_name.entered_tickets or 0,
        'total_real_tickets': form_instance.document.package_name.total_real_tickets if form_instance else document.package_name.total_real_tickets,
        'so': document_name[4] if len(document_name) > 0 else "",
        'quyenSo': document_name[2] if len(document_name) > 0 else ""
    }
    
    form_data = handle_date_fields(model_to_dict(form_instance), date_fields) if form_instance else {}
    form_data.update(common_data)
    
    return form_data


def handle_package_status(package, user, form_instance):
    entered_tickets_count = Birth_Certificate_Document.objects.filter(
        document__package_name=package, executor=user).count()
    package.entered_tickets = entered_tickets_count
    package.save()

    all_fields = [f.name for f in form_instance._meta.get_fields() if isinstance(f, Field) and not f.auto_created]
    non_empty_field_count = sum(1 for field in all_fields if getattr(form_instance, field))

    if non_empty_field_count >= form_instance.document.fields:
        form_instance.document.status_insert = 'Đã nhập'
        form_instance.document.save()

    if entered_tickets_count == package.total_real_tickets:
        package.insert_status = 'Hoàn thành nhập'
        package.save()
        
        