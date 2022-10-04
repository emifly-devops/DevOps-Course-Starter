from todo_app.helpers.trello_helpers import get_list_id


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
