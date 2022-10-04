import pytest

from todo_app.models.data.item import Item
from todo_app.models.view.items import ItemsViewModel


@pytest.fixture
def example_items_view_model():
    return ItemsViewModel(items=[
        Item(id='1', title="Task I haven't started yet", status='To Do'),
        Item(id='2', title="Task I've finished", status='Done'),
        Item(id='3', title="Task I've given up on", status='Abandoned'),
        Item(id='4', title="Task that didn't need doing after all", status='Abandoned'),
        Item(id='5', title="Task I'm still working on", status='Doing'),
        Item(id='6', title="Task I've just been given", status='To Do'),
        Item(id='7', title="Task I'm doing tomorrow", status='Doing'),
        Item(id='8', title="Task on a rogue list", status='Unknown'),
    ])


@pytest.mark.parametrize('status, matching_ids', [
    ('To Do',     ['1', '6']),
    ('Doing',     ['5', '7']),
    ('Done',      ['2']),
    ('Abandoned', ['3', '4']),
])
def test_get_items_with_status(example_items_view_model, status, matching_ids):
    filtered_items = example_items_view_model.get_items_with_status(status)
    filtered_item_ids = map(lambda item: item.id, filtered_items)
    assert sorted(filtered_item_ids) == matching_ids
