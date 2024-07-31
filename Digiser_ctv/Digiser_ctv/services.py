import os
from typing import List
from django.conf import settings
import requests
import json


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