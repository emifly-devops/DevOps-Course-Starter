from requests import request
from requests.exceptions import RequestException
from requests_oauthlib import OAuth1
from flask import current_app

trello_api_base_url = "https://api.trello.com/1"


def callable_auth_header():
    return OAuth1(client_key=current_app.config['TRELLO_KEY'], resource_owner_key=current_app.config['TRELLO_TOKEN'])


def trello_api_request(method, path, **kwargs):
    return request(method, trello_api_base_url + path, auth=callable_auth_header(), **kwargs)


valid_item_status_data = {
    'To Do': {
        'theme': 'secondary',
    },
    'Doing': {
        'theme': 'info',
    },
    'Done': {
        'theme': 'success',
    },
    'Abandoned': {
        'theme': 'danger',
    },
}


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


class Item:

    def __init__(self, title, description='', status='To Do', id=None):
        self.title = title
        self.description = description
        self.status = status
        self.id = id

    @classmethod
    def from_trello_card(cls, card, status):
        return cls(
            title=card['name'],
            description=card['desc'],
            status=status,
            id=card['id'],
        )

    def to_trello_card(self):
        return {
            'name': self.title,
            'desc': self.description,
            'idList': get_list_id(self.status),
        }


def get_items():
    """
    Fetches all saved items from the board.

    Returns:
        list: The list of saved items.
    """
    try:
        items = []
        for status in valid_item_status_data:
            list_id = get_list_id(list_name=status)
            items_in_list = map(lambda card: Item.from_trello_card(card, status),
                                trello_api_request("GET", f"/lists/{list_id}/cards").json())
            items.extend(items_in_list)
        return items
    except RequestException:
        return None


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    try:
        card = trello_api_request("GET", f"/cards/{id}").json()
        list_containing_card = trello_api_request("GET", f"/lists/{card['idList']}").json()
        item = Item.from_trello_card(card=card, status=list_containing_card['name'])
        return item
    except RequestException:
        return None


def add_item(title):
    """
    Adds a new item with the specified title to the board.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    item = Item(title)
    try:
        response_card = trello_api_request("POST", "/cards", data=item.to_trello_card()).json()
        return Item.from_trello_card(response_card, item.status)
    except RequestException:
        return None


def save_item(item):
    """
    Updates an existing item on the board. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.

    Returns:
        item: The updated item.
    """
    try:
        response_card = trello_api_request("PUT", f"/cards/{item.id}", data=item.to_trello_card()).json()
        return Item.from_trello_card(response_card, item.status)
    except RequestException:
        return None


def remove_item(id):
    """
    Removes the item with the specified ID from the board. If no item matches the specified ID, nothing is removed.

    Args:
        id: The ID of the item to delete.
    """
    try:
        trello_api_request("DELETE", f"/cards/{id}")
    except RequestException:
        pass
