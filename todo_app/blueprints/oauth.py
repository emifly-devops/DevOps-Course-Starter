import os

from flask_dance.contrib.github import make_github_blueprint

oauth_blueprint = make_github_blueprint(
    client_id=os.environ.get('OAUTH_CLIENT_ID'),
    client_secret=os.environ.get('OAUTH_CLIENT_SECRET'),
)
