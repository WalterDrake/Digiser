import os
import gspread
from typing import List
from django.conf import settings
import requests
import json


def initialize_gspread() -> gspread.client.Client:
    """
    Initialize a gspread client with the given credentials.
    """
    return gspread.service_account_from_dict(get_credentials())  # Note: we could move this to settings to do this once.


def send_zalo_oa_message_to_client(user_id: str, message: str):
    access_token = os.getenv("ZALO_OA_ACCESS_TOKEN")

    headers = {'Content-Type': 'application/json','access_token': access_token}

    body = {
        'recipient': {
            "user_id": f"{user_id}"
        },
        "message": {
            "text": message
        }
    }

    url = "https://openapi.zalo.me/v3.0/oa/message/cs"

    response = requests.post(url, headers=headers, json=body)
    print(response.status_code)
    print(response.json())


def find_id_with_username(username: str):
    access_token = os.getenv("ZALO_OA_ACCESS_TOKEN")
    params={'data': json.dumps({"offset": 0, "count": 5, "tag_name": "Chưa đăng ký"})}
    headers = {'access_token': access_token}
    url='https://openapi.zalo.me/v3.0/oa/user/getlist'
    # Sending GET request with parameters
    response = requests.get(url, headers=headers, params=params)
    user_list = response.json()['data']['users']
    for user in user_list:
        user_info = get_user_info_with_id(user['user_id'])
        if (user_info['data']['display_name'] == username):
            return {"data": user['user_id']}
    return {"data": "none"}

def get_user_info_with_id(user_id: str):
    access_token = os.getenv("ZALO_OA_ACCESS_TOKEN")
    params = {'data': json.dumps({"user_id": user_id})}
    headers = {'access_token': access_token}
    url='https://openapi.zalo.me/v3.0/oa/user/detail'
    # Sending GET request with parameters
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_credentials() -> dict:
    """
    Return gspread credentials.
    """
    return {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": os.getenv("PRIVATE_KEY"),
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN")
    }


def get_all_rows(doc_name: str, sheet_id: int = None) -> List[dict]:
    """
    Fetches all rows from a given Google Sheet worksheet.
    """
    sh = settings.GSPREAD_CLIENT.open(doc_name)
    worksheet = sh.get_worksheet(sheet_id) if sheet_id else sh.get_worksheet(0)
    return worksheet.get_all_records()


def add_row(doc_name: str, sheet_id: id = None, last_row: int = None, formatted_data: dict[str, any] = None):
    """
    Add row from a given Google Sheet worksheet.
    """
    try:
        sh = settings.GSPREAD_CLIENT.open(doc_name)
        worksheet = sh.get_worksheet(
            sheet_id) if sheet_id else sh.get_worksheet(0)
        print(formatted_data)
        worksheet.update(f'A{last_row+1}:Q{last_row+1}',
                         [[
                           formatted_data['ID'],
                           formatted_data['password'],
                           formatted_data['gmail'],
                           formatted_data['phone'],
                           formatted_data['full name'],
                           formatted_data['birthday'],
                           formatted_data['address'],
                           formatted_data['qualification'],
                           formatted_data['identification'],
                           formatted_data['identification address'],
                           formatted_data['note'],
                           formatted_data['role'],
                           formatted_data['account number'],
                           formatted_data['bank name'],
                           formatted_data['branch'],
                           formatted_data['owner'],
                           formatted_data['code bank'],
                           ]])
        return {"Response": "Success"}
    except Exception as e:
        return {"Response": e}


def count_row(doc_name: str, sheet_id: int = None):
    try:
        sh = settings.GSPREAD_CLIENT.open(doc_name)
        worksheet = sh.get_worksheet(
            sheet_id) if sheet_id else sh.get_worksheet(0)
        cnt = len(worksheet.col_values(1))
        return cnt
    except Exception as e:
        raise e

# def add_row(doc_name:str, sheet_name: str = None, records: List[dict] = None, formatted_data: dict[str, any] = None):
#   """
#   Update row from a given Google Sheet worksheet.
#   """
#   try:
#     sh = settings.GSPREAD_CLIENT.open(doc_name)
#     worksheet = sh.worksheet[sheet_name] if sheet_name else sh.get_worksheet(0)
#     for i, record in enumerate(records):
#       if record['MaNV'] == formatted_data['MaNV']:
#       # Update the entire row with the new data
#           row = i + 2  # Adjust for header row (indexing starts from 0)
#           worksheet.update(f'A{row}:E{row}', [[
#               formatted_data['MaNV'],
#               formatted_data['Ten'],
#               formatted_data['CCCD'],
#               formatted_data['Email'],
#               formatted_data['Role']
#       ]])
#     return {"Response":"Success"}
#   except Exception as e:
#     return {"Response": e.message}
