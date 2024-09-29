from authentication.models import CustomUser
from django.db.models import Max, Sum
from project.models.model1 import Package_detail, Document
import json
from .models import Salary


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

    def set_dates(package_detail, role):
        if role == 'inserter':
            return package_detail.start_insert.strftime('%d/%m/%Y'), package_detail.finish_insert.strftime('%d/%m/%Y')
        return package_detail.start_check.strftime('%d/%m/%Y'), package_detail.finish_check.strftime('%d/%m/%Y')

    # Iterate through each datum (package)
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
        
        # Determine the role (inserter/checker) and set the received/deadline days
        if package_detail:
            if package_detail.inserter and user.full_name == package_detail.inserter.full_name:
                package_info['received_day'], package_info['deadline_day'] = set_dates(package_detail, 'inserter')
            elif package_detail.checker_1 and user.full_name == package_detail.checker_1.full_name:
                package_info['received_day'], package_info['deadline_day'] = set_dates(package_detail, 'checker')
            elif package_detail.checker_2 and user.full_name == package_detail.checker_2.full_name:
                package_info['received_day'], package_info['deadline_day'] = set_dates(package_detail, 'checker')
        
        # Collect documents related to the package
        related_documents = documents_dict.get(package_name, [])
        for document in related_documents:
            # Determine the executor and status based on role
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


def statistic_salary(user):
    total_salary = Salary.objects.filter(user=user).aggregate(Sum('final_salary'))['final_salary__sum']
    if total_salary is None:
        return 0
    return f"{total_salary:,}"

def statistic_project(user):
    total_project_details = Salary.objects.filter(user=user).count()
    return total_project_details

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