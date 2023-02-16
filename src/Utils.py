import requests
import json

from Exceptions import InvalidRequest
from Config import _Key


def get(url, payload=None):
    """
    Used to make a call to an API.

    :param payload:
    :param url:
    :return:
    """
    response = json.loads(requests.post(url, json=payload).text)
    if "errors" in response.keys():
        raise InvalidRequest(response, payload)
    return response


def get_v3(request):
    """
    Used to make a call to APIv3

    :param request: The APIv3 request desired
    """
    return get(f"https://api.politicsandwar.com/graphql?api_key={_Key}", {"query": request})["data"]


def war_range(score: int):
    return score*0.75, score*1.75


def espionage_range(score: int):
    return score*0.4, score*2.50
