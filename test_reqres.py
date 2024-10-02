import json
import requests
import pytest
from jsonschema import validate



base_url = "https://api1.setmeter.ru/api/v1"
exp_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1lZGlhc2NvcGVfYXBpIiwic2NvcGUiOiJhY2Nlc3MiLCJpYXQiOjE3MTYzODQyNTQsImV4cCI6MTcxNjM4Nzg1NH0.E1PsOkpzaiXpwvzuHw8VQvbcDPSY8tU4LdsW2kqIGvY'


def test_get_positive_token():
    payload = {"username": "mediascope_api", "password": "p3C36dpFg%zNMkVxByqy"}

    response = requests.post(f"{base_url}/auth/token", data=payload)
    body_dict = json.loads(response.text)
    token_str = body_dict['access_token']
    print(token_str)

    assert response.status_code == 200


@pytest.fixture()
def get_token():
    payload = {"username": "mediascope_api", "password": "p3C36dpFg%zNMkVxByqy"}

    response = requests.post(f"{base_url}/auth/token", data=payload)
    body = response.json()
    body_dict = json.loads(response.text)
    token_str = body_dict['access_token']
    real_bearer = 'Bearer ' + token_str
    print(real_bearer)

    assert response.status_code == 200

    with open("token_schema.json") as file:
        validate(body, schema=json.loads(file.read()))

    return real_bearer



def test_get_positive_my_login_data(get_token):
    response = requests.get(f"{base_url}/users/me", headers={'authorization': get_token})
    body = response.json()
    print(response.text)

    assert response.status_code == 200



    with open("user.json") as file:
        validate(body, schema=json.loads(file.read()))


def test_get_negative_expired_token():
    response = requests.get(f"{base_url}/users/me", headers={'authorization': exp_token})
    body = response.json()
    print(response.status_code)
    print(response.text)
    print(response.headers)

    assert response.status_code == 401

def test_get_positive_existing_device_data(get_token):
    response = requests.get(f"{base_url}/users/stlw455wpb", headers={'authorization': get_token})
    body = response.json()
    print(response.text)

    assert response.status_code == 200

    with open("device.json") as file:
         validate(body, schema=json.loads(file.read()))

def test_get_positive_users_data(get_token):
    response = requests.get(f"{base_url}/users", headers={'authorization': get_token})
    body = response.json()
    print(response.text)

    assert response.status_code == 200

def test_get_negative_non_existing_device(get_token):
    response = requests.get(f"{base_url}/users/zzzz", headers={'authorization': get_token})
    print(response.text)

    assert response.status_code == 404

def test_get_positive_existing_device_activity(get_token):
    response = requests.get(f"{base_url}/users/stlw455wpb/activity", headers={'authorization': get_token})
    body = response.json()
    print(response.text)

    assert response.status_code == 200

    with open("activity.json") as file:
         validate(body, schema=json.loads(file.read()))