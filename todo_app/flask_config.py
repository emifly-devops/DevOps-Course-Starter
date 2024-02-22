import os


class Config:

    def __init__(self):
        config_vars = [
            'SECRET_KEY',
            'MONGO_URI',
        ]
        for config_var in config_vars:
            setattr(self, config_var, os.environ.get(config_var))
            if not getattr(self, config_var):
                raise ValueError(f"{config_var} not set for Flask application.")
