from flask import Flask

def configure(app: Flask):
    from .reservation import bp_admin
    app.register_blueprint(bp_admin)
