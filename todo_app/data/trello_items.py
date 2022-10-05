from requests.exceptions import RequestException

from todo_app.helpers.trello_helpers import trello_api_request, get_list_id_from_name
from todo_app.models.data.item import Item


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


def get_items():
    """
    Fetches all saved items from the board.

    Returns:
        list: The list of saved items.
    """
    try:
        items = []
        for status in valid_item_status_data:
            list_id = get_list_id_from_name(list_name=status)
            items_in_list = map(Item.from_trello_card, trello_api_request("GET", f"/lists/{list_id}/cards").json())
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
        item = Item.from_trello_card(card)
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
        return Item.from_trello_card(response_card)
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
        return Item.from_trello_card(response_card)
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
