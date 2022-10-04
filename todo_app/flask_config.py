import os


class Config:
    def __init__(self):
        trello_config_vars = [
            'TRELLO_KEY',
            'TRELLO_TOKEN',
            'TRELLO_BOARD_ID',
        ]
        for config_var in trello_config_vars:
            setattr(self, config_var, os.environ.get(config_var))
            if not getattr(self, config_var):
                raise ValueError(f"{config_var} not set for Flask application.")
