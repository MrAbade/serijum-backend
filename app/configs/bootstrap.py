from flask import Flask
from flask_bootstrap import Bootstrap


def configure(app: Flask):
    Bootstrap(app)
    
    return app
