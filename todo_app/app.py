from flask import Flask, render_template, redirect, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, get_item, add_item, save_item, \
    valid_item_statuses, valid_item_status_data

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = sorted(get_items(), key=lambda item: valid_item_statuses.index(item['status']))
    return render_template('index.html', items=items, item_status_data=valid_item_status_data)


@app.route('/', methods=['POST'])
def create_item():
    title = request.form.get('title')
    if title and title.strip():
        add_item(title)
    return redirect('/')


@app.route('/update/<int:item_id>/status/<string:item_status>')
def update_item_status(item_id, item_status):
    item = get_item(item_id)
    if item is not None and item_status in valid_item_statuses:
        item['status'] = item_status
        save_item(item)
    return redirect('/')
