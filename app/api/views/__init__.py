from flask import Blueprint

bp_index = Blueprint('index', __name__)

@bp_index.route('/')
def index():
    return """
    <html>
        <h1>Boa maluco! Abade na area!</h1>
    </html>
    """

def configure(app):
    app.register_blueprint(bp_index)

    from .user import bp_user
    app.register_blueprint(bp_user)

    from .suite import bp_suite
    app.register_blueprint(bp_suite)

    from .schedule import bp_schedule
    app.register_blueprint(bp_schedule)
