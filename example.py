import json
import requests
import pytest
from jsonschema import validate
from selene.support.conditions.have import values
from schemas import post_users

url = "https://reqres.in/api"

payload = {"name": "morpheus", "job": "leader"}

response = requests.request("POST", url, data=payload)

print(response.text)
exp_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1lZGlhc2NvcGVfYXBpIiwic2NvcGUiOiJhY2Nlc3MiLCJpYXQiOjE3MTYzODQyNTQsImV4cCI6MTcxNjM4Nzg1NH0.E1PsOkpzaiXpwvzuHw8VQvbcDPSY8tU4LdsW2kqIGvY'

@pytest.fixture()
def say_hello():
    print('hello')


def test_schema_validate_from_file(say_hello):
    response = requests.post("https://reqres.in/api/users", data={"name": "morpheus", "job": "master"})
    body = response.json()
    print(response.text)
    print(response.status_code)

    assert response.status_code == 201
    with open("post_users.json") as file:
        validate(body, schema=json.loads(file.read()))


def test_schema_validate_from_variable():
    response = requests.post("https://reqres.in/api/users", data={"name": "morpheus", "job": "master"})
    body = response.json()

    assert response.status_code == 201
    validate(body, schema=post_users)


def test_job_name_from_request_returns_in_response():
    job = "master"
    name = "morpheus"

    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job})
    body = response.json()
    print(body)

    assert body["name"] == name
    assert body["job"] == job


def test_get_users_returns_unique_users():
    response = requests.get(
        url="https://reqres.in/api/users",
        params={"page": 2, "per_page": 4},
        verify=False
    )
    print(response.text)
    ids = [element["id"] for element in response.json()["data"]]

    assert len(ids) == len(set(ids))
    print(len(ids))

base_url = "https://api1.setmeter.ru/api/v1"
exp_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1lZGlhc2NvcGVfYXBpIiwic2NvcGUiOiJhY2Nlc3MiLCJpYXQiOjE3MTYzODQyNTQsImV4cCI6MTcxNjM4Nzg1NH0.E1PsOkpzaiXpwvzuHw8VQvbcDPSY8tU4LdsW2kqIGvY'


def test_get_positive_token():
    payload = {"username": "mediascope_api", "password": "p3C36dpFg%zNMkVxByqy"}

    response = requests.post(f"{base_url}/auth/token", data=payload)
    body = response.json()
    #print(response.text)
    #print(body)
    # print(response.status_code)
    # print(response.headers)
    body_dict = json.loads(response.text)
    token_str = body_dict['access_token']
    print(token_str)
    real_bearer = 'Bearer ' + token_str
    assert response.status_code == 200