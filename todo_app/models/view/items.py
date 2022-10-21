from todo_app.data.trello_items import valid_item_status_data


class ItemsViewModel:

    def __init__(self, items):
        self.items = items
        self.item_status_data = valid_item_status_data

    def get_items_with_status(self, status):
        return list(filter(lambda item: item.status == status, self.items)) if self.items else None
