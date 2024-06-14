import os
import gspread
from typing import List
from django.conf import settings


def initialize_gspread() -> gspread.client.Client:
    """
    Initialize a gspread client with the given credentials.
    """
    return gspread.service_account_from_dict(get_credentials())  # Note: we could move this to settings to do this once.


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
        print(worksheet)
        print(formatted_data)
        worksheet.update(f'A{last_row+1}:C{last_row+1}',
                         [[
                           formatted_data['ID'],
                           formatted_data['password'],
                           formatted_data['gmail']
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
