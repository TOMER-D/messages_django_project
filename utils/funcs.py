from django.http import HttpRequest
import json


def check_missing_fields(**kwargs) -> list:
    return [key for key in kwargs if kwargs[key] is None]


def read_request(request: HttpRequest) -> dict:
    data = {}
    if request.body:
        data = json.loads(request.body)
    return data
