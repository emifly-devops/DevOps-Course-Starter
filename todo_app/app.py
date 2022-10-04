from flask import Flask, render_template, redirect, request

from todo_app.flask_config import Config
from todo_app.data.trello_items import valid_item_status_data, get_items, get_item, add_item, save_item, remove_item
from todo_app.models.view.items import ItemsViewModel

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    items_view_model = ItemsViewModel(items)
    return render_template('index.html', view_model=items_view_model)


@app.route('/create', methods=['POST'])
def create_item():
    title = request.form.get('title')
    if title is not None:
        add_item(title)
    return redirect('/')


@app.route('/update/<item_id>', methods=['POST'])
def update_item(item_id):
    item = get_item(item_id)
    if item is not None:
        if (item_title := request.form.get('title')) is not None:
            item.title = item_title
        if (item_description := request.form.get('description')) is not None:
            item.description = item_description
        if (item_status := request.form.get('status')) in valid_item_status_data:
            item.status = item_status
        save_item(item)
    return redirect('/')


@app.route('/delete/<item_id>', methods=['POST'])
def delete_item(item_id):
    remove_item(item_id)
    return redirect('/')
