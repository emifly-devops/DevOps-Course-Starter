import os
import pytest
import requests
from dotenv import find_dotenv, load_dotenv

from todo_app.app import create_app
from todo_app.helpers.trello_helpers import trello_api_base_url


test_to_do_card = {
    'id': 'test-card-1',
    'name': 'Task I have not started yet',
    'desc': 'This one looks tricky',
    'idList': 'test-list-1',
}
test_doing_card = {
    'id': 'test-card-2',
    'name': 'Task I am partway through',
    'desc': 'This is taking a while',
    'idList': 'test-list-2',
}
test_done_card = {
    'id': 'test-card-3',
    'name': 'Task I have finished',
    'desc': 'This went well',
    'idList': 'test-list-3',
}

test_to_do_list = {
    'id': 'test-list-1',
    'name': 'To Do',
    'cards': [test_to_do_card],
}
test_doing_list = {
    'id': 'test-list-2',
    'name': 'Doing',
    'cards': [test_doing_card],
}
test_done_list = {
    'id': 'test-list-3',
    'name': 'Done',
    'cards': [test_done_card],
}


@pytest.fixture
def client():
    dotenv_test_file_path = find_dotenv('.env.test')
    load_dotenv(dotenv_test_file_path, override=True)
    test_app = create_app()
    with test_app.test_client() as client:
        yield client


class StubResponse:

    def __init__(self, fake_response_data=None):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

    def raise_for_status(self):
        pass


def request_stub(method, url, **kwargs):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')

    # Board endpoints
    if method == "GET" and url == f"{trello_api_base_url}/boards/{test_board_id}/lists":
        return StubResponse(fake_response_data=[test_to_do_list, test_doing_list, test_done_list])
    if method == "POST" and url == f"{trello_api_base_url}/boards/{test_board_id}/lists":
        return StubResponse(fake_response_data={**kwargs['data'], 'id': 'test-list-new'})

    # List endpoints
    for test_list in [test_to_do_list, test_doing_list, test_done_list]:
        if method == "GET" and url == f"{trello_api_base_url}/lists/{test_list['id']}":
            return StubResponse(fake_response_data=test_list)
        if method == "GET" and url == f"{trello_api_base_url}/lists/{test_list['id']}/cards":
            return StubResponse(fake_response_data=test_list['cards'])
    if method == "GET" and url == f"{trello_api_base_url}/lists/test-list-new/cards":
        return StubResponse(fake_response_data=[])

    # Card endpoints
    if method == "POST" and url == f"{trello_api_base_url}/cards" \
            and all(key in kwargs['data'] for key in ['name', 'desc', 'idList']):
        return StubResponse(fake_response_data={**kwargs['data'], 'id': 'test-card-new'})
    for test_card in [test_to_do_card, test_doing_card, test_done_card]:
        if method == "GET" and url == f"{trello_api_base_url}/cards/{test_card['id']}":
            return StubResponse(fake_response_data=test_card)
        if method == "PUT" and url == f"{trello_api_base_url}/cards/{test_card['id']}" \
                and any(key in kwargs['data'] for key in ['name', 'desc', 'idList']):
            return StubResponse(fake_response_data={**test_card, **kwargs['data']})
        if method == "DELETE" and url == f"{trello_api_base_url}/cards/{test_card['id']}":
            return StubResponse()


def test_index(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', request_stub)

    response = client.get("/")
    assert response.status_code == 200

    page_content = response.data.decode()
    assert test_to_do_card['name'] in page_content
    assert test_to_do_card['desc'] in page_content
    assert test_doing_card['name'] in page_content
    assert test_doing_card['desc'] in page_content
    assert test_done_card['name'] in page_content
    assert test_done_card['desc'] in page_content


def test_create_item(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', request_stub)

    response = client.post("/create", data={'title': 'New task'})
    assert response.status_code == 302


def test_update_item(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', request_stub)

    response = client.post(f"/update/{test_to_do_card['id']}", data={'title': 'Altered task', 'desc': 'Altered description'})
    assert response.status_code == 302

    response = client.post(f"/update/{test_to_do_card['id']}", data={'idList': test_doing_list['id']})
    assert response.status_code == 302


def test_delete_item(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', request_stub)

    response = client.post(f"/delete/{test_to_do_card['id']}")
    assert response.status_code == 302
