class Item:

    def __init__(self, title, description='', status='To Do', id=None):
        self.title = title
        self.description = description
        self.status = status
        self.id = id

    @classmethod
    def from_mongo_item(cls, item):
        return cls(
            title=item['title'],
            description=item['description'],
            status=item['status'],
            id=item['_id'],
        )

    def to_mongo_item(self):
        return {
            'title': self.title,
            'description': self.description,
            'status': self.status,
        }
