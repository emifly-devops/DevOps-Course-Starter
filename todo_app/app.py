import os

from flask import Flask, render_template, redirect, request
from werkzeug.routing import BaseConverter
import pymongo
from dotenv import find_dotenv, load_dotenv

from todo_app.flask_config import Config
from todo_app.models.view.items_view_model import ItemsViewModel
from todo_app.repositories.item_repo import ItemRepo

if os.environ.get('FLASK_DEBUG') or os.environ.get('FLASK_TESTING'):
    env_file_path = find_dotenv('.env.devtest')
    load_dotenv(env_file_path, override=True)


class ItemIdConverter(BaseConverter):
    regex = r"[0-9a-f]{24}"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.url_map.converters['item_id'] = ItemIdConverter

    item_repo = ItemRepo(pymongo.MongoClient(app.config['MONGO_URI']))

    @app.route('/')
    def index():
        items = item_repo.get_all()
        items_view_model = ItemsViewModel(items)
        return render_template('index.html', view_model=items_view_model)

    @app.route('/create', methods=['POST'])
    def create_item():
        title = request.form.get('title')
        if title is not None:
            item_repo.create(title)
        return redirect('/')

    @app.route('/update/<item_id:item_id>', methods=['POST'])
    def update_item(item_id):
        item_repo.update(item_id, request.form)
        return redirect('/')

    @app.route('/delete/<item_id:item_id>', methods=['POST'])
    def delete_item(item_id):
        item_repo.delete(item_id)
        return redirect('/')

    return app
