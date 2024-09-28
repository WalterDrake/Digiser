from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.html import escape
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import *
from .models.model2 import *
from .models.model1 import Document, Package_detail, Package
from authentication.models import CustomUser
import hashlib, zipfile, io
from django.db.models import Q
import pandas as pd

@login_required
def form_redirect(request, **kwargs):
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
    

def package_redirect(request):
    if request.method == 'POST':
        package_name = request.POST.get('package_name')
        idx = request.POST.get('idx')
        # Ensure the package_name is not None
        if package_name:
            # Create a SHAKE-128 hash object
            shake = hashlib.shake_128()

            # Update the hash object with the byte-encoded data
            shake.update(package_name.encode('utf-8'))

            # Generate a 8-byte digest
            digest = shake.digest(8)

            redirect_url = f'/document/{digest.hex()}/{idx}'

            # Return the URL in the JSON response
            return JsonResponse({'redirect_url': redirect_url})
        
        return JsonResponse({'status': 'error', 'message': 'No package_name provided'})
    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

@user_passes_test(is_superuser)
@login_required
def export_package(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User ID is required'})

        try:
            user = CustomUser.objects.get(code=user_id)  # Assuming user_code is unique
            packages = Package_detail.objects.filter(Q(checker_1=user) | Q(checker_2=user)) 

            if not packages.exists():
                return JsonResponse({'status': 'error', 'message': 'No packages found for the provided user ID'})
            
            # Create an in-memory output file for the ZIP file
            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for package in packages:
                    documents = Document.objects.select_related('package_name').filter(package_name=package.package_name)

                    if documents.exists():
                        # Find birth certificate documents where the executor is the user
                        birth_certificate_documents = Birth_Certificate_Document.objects.select_related('executor').prefetch_related('document').filter(
                            document__in=documents,
                            executor=user
                        )

                        if birth_certificate_documents.exists():
                            df = birth_certificate_documents_to_df(birth_certificate_documents)

                            try:
                                excel_buffer = io.BytesIO()
                                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                    df.to_excel(writer, sheet_name='Sheet1', index=False)
                                excel_buffer.seek(0)  # Ensure the buffer is ready for reading
                            except Exception as e:
                                print(f"Error writing Excel file: {e}")

                            # Construct the directory structure
                            package_name_str = str(package.package_name)
                            package_name_parts = package_name_str.split('_')
                            if len(package_name_parts) >= 3:
                                folder1 = package_name_parts[2][:2]
                                folder2 = package_name_parts[2][2:]
                                folder3 = package_name_parts[3]
                                file_name = f"{birth_certificate_documents[0].document.document_name[:-8]}.xlsx"

                                # Add Excel file to the ZIP
                                zip_file.writestr(f"{folder1}/{folder2}/{folder3}/{file_name}", excel_buffer.getvalue())
                            else:
                                print(f"Package name structure is incorrect for package: {package.package_name}")

            zip_buffer.seek(0)

             # Create the HTTP response
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=exported_packages.zip'
            return response
        
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'})
    
    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})
        


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

    # Handling POST request
    if request.method == 'POST':
        form_data = getattr(request, 'form_data', None)
        error_list = getattr(request, 'error_list', None)
        
        if error_list:
            form_data.update(get_form_data_choices())
            form_data.update(prepare_form_data(document, date_fields=date_fields))
            return render(request, 'pages/form.html', {'form': form_data, 'form_type': 'birth_cert', 'error_list': error_list})
        
        form_data['executor'] = user
        form_instance, _ = Birth_Certificate_Document.objects.update_or_create(
            document=document, executor=user, defaults=form_data)

        if role == 'inserter' and package_detail_name:
            package = Package.objects.filter(package_name=package_detail_name).first()
            if package:
                handle_package_status(package, user, form_instance)

        form_data.update(get_form_data_choices())
        form_data.update(prepare_form_data(document, form_instance=form_instance, date_fields=date_fields))
        return render(request, 'pages/form.html', {'form': form_data, 'form_type': 'birth_cert', 'error_list': None})

    # Handling GET request
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

    form_data = get_form_data_choices()
    form_data.update(prepare_form_data(document, form_instance=form_instance, lock=lock, date_fields=date_fields))
    return render(request, 'pages/form.html', {'form': form_data, 'form_type': 'birth_cert'})


