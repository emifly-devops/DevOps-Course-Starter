from requests import request
from requests_oauthlib import OAuth1
from flask import current_app
from functools import lru_cache

trello_api_base_url = "https://api.trello.com/1"


def callable_auth_header():
    return OAuth1(client_key=current_app.config['TRELLO_KEY'], resource_owner_key=current_app.config['TRELLO_TOKEN'])


def trello_api_request(method, path, **kwargs):
    return request(method, trello_api_base_url + path, auth=callable_auth_header(), **kwargs)


@lru_cache(maxsize=None)
def get_list_id(list_name):
    board_lists = trello_api_request("GET", f"/boards/{current_app.config['TRELLO_BOARD_ID']}/lists").json()
    try:
        return next(filter(lambda board_list: board_list['name'] == list_name, board_lists))['id']
    except StopIteration:
        list_to_add = {
            'name': list_name,
            'pos': 'bottom',
        }
        return trello_api_request("POST", f"/boards/{current_app.config['TRELLO_BOARD_ID']}/lists", data=list_to_add).json()['id']
