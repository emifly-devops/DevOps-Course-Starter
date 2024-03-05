import os

from flask import Flask, render_template, redirect, request, flash
from flask_dance.contrib.github import github
from werkzeug.routing import BaseConverter
import pymongo
from pymongo.errors import PyMongoError
from dotenv import find_dotenv, load_dotenv

from todo_app.flask_config import Config
from todo_app.blueprints.oauth import oauth_blueprint
from todo_app.models.view.items_view_model import ItemsViewModel
from todo_app.repositories.item_repo import ItemRepo
from todo_app.helpers.decorators import login_required, logout_required

if os.environ.get('FLASK_DEBUG') or os.environ.get('FLASK_TESTING'):
    env_file_path = find_dotenv('.env.public')
    load_dotenv(env_file_path, override=True)


class ItemIdConverter(BaseConverter):
    regex = r"[0-9a-f]{24}"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.url_map.converters['item_id'] = ItemIdConverter
    app.register_blueprint(oauth_blueprint, url_prefix='/login')

    item_repo = ItemRepo(pymongo.MongoClient(app.config['MONGO_URI']))

    @app.context_processor
    def add_auth_status_to_context():
        return dict(authorized=github.authorized)

    @app.route('/login')
    @logout_required
    def login():
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        del oauth_blueprint.token
        return redirect('/login')

    @app.route('/')
    @login_required
    def index():
        try:
            items = item_repo.get_all()
        except PyMongoError:
            items = None
            flash("Unable to retrieve items at this time. Please try again later.")
        items_view_model = ItemsViewModel(items)
        return render_template('index.html', view_model=items_view_model)

    @app.route('/create', methods=['POST'])
    @login_required
    def create_item():
        title = request.form.get('title')
        if title is not None:
            try:
                item_repo.create(title)
            except PyMongoError:
                flash("Unable to create item at this time. Please try again later.")
        return redirect('/')

    @app.route('/update/<item_id:item_id>', methods=['POST'])
    @login_required
    def update_item(item_id):
        try:
            item_repo.update(item_id, request.form)
        except PyMongoError:
            flash("Unable to update item at this time. Please try again later.")
        return redirect('/')

    @app.route('/delete/<item_id:item_id>', methods=['POST'])
    @login_required
    def delete_item(item_id):
        try:
            item_repo.delete(item_id)
        except PyMongoError:
            flash("Unable to delete item at this time. Please try again later.")
        return redirect('/')

    return app
