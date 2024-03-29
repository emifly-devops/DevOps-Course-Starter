from bson.objectid import ObjectId

from todo_app.models.data.item import Item


class ItemRepo:

    def __init__(self, context):
        self.context = context

    def get_all(self):
        """
        Fetches all saved items from the database.

        Returns:
            items: The list of saved items.
        """
        return [Item.from_mongo_item(item) for item in self.context.todo_app.items.find()]

    def create(self, title):
        """
        Adds a new item with the specified title to the database.

        Args:
            title: The title of the item to create.
        """
        self.context.todo_app.items.insert_one(Item(title).to_mongo_item())

    def update(self, id, changes):
        """
        Updates an existing item in the database.
        If no existing item matches the ID of the specified item, nothing is saved.

        Args:
            id: The ID of the item to update.
            changes: Any changes to apply to the item.
        """
        self.context.todo_app.items.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                property: changes[property]
                for property in {'title', 'description', 'status'}.intersection(changes)
            }}
        )

    def delete(self, id):
        """
        Removes the item with the specified ID from the database.
        If no item matches the specified ID, nothing is removed.

        Args:
            id: The ID of the item to delete.
        """
        self.context.todo_app.items.delete_one({'_id': ObjectId(id)})
