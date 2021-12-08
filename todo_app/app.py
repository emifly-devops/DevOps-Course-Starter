from flask import Flask, render_template, redirect, request

from todo_app.flask_config import Config
from todo_app.data.session_items import valid_item_statuses, valid_item_status_data, \
    get_items, get_item, add_item, save_item, remove_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = sorted(reversed(get_items()), key=lambda item: valid_item_statuses.index(item['status']))
    return render_template('index.html', items=items, item_status_data=valid_item_status_data)


@app.route('/', methods=['POST'])
def create_item():
    title = request.form.get('title')
    if title is not None and title.strip():
        add_item(title.strip())
    return redirect('/')


@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    item = get_item(item_id)
    item_status = request.form.get('status')
    if item is not None and item_status in valid_item_statuses:
        item['status'] = item_status
        save_item(item)
    return redirect('/')


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    remove_item(item_id)
    return redirect('/')
