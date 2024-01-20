class ItemsViewModel:
    item_status_data = {
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

    def __init__(self, items):
        self.items = items

    def get_items_with_status(self, status):
        return [item for item in self.items if item.status == status] if self.items is not None else None
