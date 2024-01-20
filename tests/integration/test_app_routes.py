import os
from bson.objectid import ObjectId

import pytest
import pymongo
import mongomock
from dotenv import find_dotenv, load_dotenv

test_mongo_to_do_item = {
    '_id': ObjectId('1d28f892a5408afb535797e0'),
    'title': 'Task I have not started yet',
    'description': 'This one looks tricky',
    'status': 'To Do',
}
test_mongo_doing_item = {
    '_id': ObjectId('2700338fe4fc83f4750bf57f'),
    'title': 'Task I am partway through',
    'description': 'This is taking a while',
    'status': 'Doing',
}
test_mongo_done_item = {
    '_id': ObjectId('33bfdd95e5f75a19a99f1fe1'),
    'title': 'Task I have finished',
    'description': 'This went well',
    'status': 'Done',
}

test_mongo_items = [
    test_mongo_to_do_item,
    test_mongo_doing_item,
    test_mongo_done_item,
]


def single(iterator):
    # Check for at least one item
    try:
        next(iterator)
    except StopIteration:
        return False
    # Check for no more than one item
    try:
        next(iterator)
    except StopIteration:
        return True
    else:
        return False


@pytest.fixture
def client():
    flaskenv_file_path = find_dotenv('.flaskenv.test')
    load_dotenv(flaskenv_file_path)

    from todo_app.app import create_app

    with mongomock.patch(servers=os.environ.get('MONGO_URI')):
        mongo_client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
        mongo_client.todo_app.items.insert_many(test_mongo_items)
        test_app = create_app()
        with test_app.test_client() as test_client:
            yield test_client


def test_index(client):
    # Act
    response = client.get("/")
    page_content = response.data.decode()

    # Assert
    assert response.status_code == 200
    assert test_mongo_to_do_item['title'] in page_content
    assert test_mongo_to_do_item['description'] in page_content
    assert test_mongo_doing_item['title'] in page_content
    assert test_mongo_doing_item['description'] in page_content
    assert test_mongo_done_item['title'] in page_content
    assert test_mongo_done_item['description'] in page_content


def test_create_item(client):
    # Arrange
    mongo_client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
    task_creation_data = {'title': 'New task'}
    assert not any(mongo_client.todo_app.items.find(task_creation_data))

    # Act
    response = client.post("/create", data=task_creation_data)

    # Assert
    assert response.status_code == 302
    assert single(mongo_client.todo_app.items.find(task_creation_data))


def test_update_item(client):
    # Arrange
    mongo_client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
    task_update_data_1 = {'title': 'Altered task', 'description': 'Altered description'}
    task_update_data_2 = {'status': 'abandoned'}
    assert single(mongo_client.todo_app.items.find(test_mongo_to_do_item))
    assert single(mongo_client.todo_app.items.find(test_mongo_doing_item))
    assert not any(mongo_client.todo_app.items.find(task_update_data_1))
    assert not any(mongo_client.todo_app.items.find(task_update_data_2))

    # Act
    response_1 = client.post(f"/update/{test_mongo_to_do_item['_id']}", data=task_update_data_1)
    response_2 = client.post(f"/update/{test_mongo_doing_item['_id']}", data=task_update_data_2)

    # Assert
    assert response_1.status_code == 302
    assert response_2.status_code == 302
    assert not any(mongo_client.todo_app.items.find(test_mongo_to_do_item))
    assert not any(mongo_client.todo_app.items.find(test_mongo_doing_item))
    assert single(mongo_client.todo_app.items.find({**test_mongo_to_do_item, **task_update_data_1}))
    assert single(mongo_client.todo_app.items.find({**test_mongo_doing_item, **task_update_data_2}))


def test_delete_item(client):
    # Arrange
    mongo_client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
    initial_items_len = len(list(mongo_client.todo_app.items.find()))

    # Act
    response = client.post(f"/delete/{test_mongo_to_do_item['_id']}")

    # Assert
    assert response.status_code == 302
    assert not any(mongo_client.todo_app.items.find({'_id': test_mongo_to_do_item['_id']}))
    assert len(list(mongo_client.todo_app.items.find())) == initial_items_len - 1
