from flask import Flask


def configure(app: Flask):
    from .authentication import bp_auth
    app.register_blueprint(bp_auth, url_prefix='/auth')

    from .view_reservation import bp_reservation
    app.register_blueprint(bp_reservation, url_prefix='/suites')
    
    from .book_release import bp_book_release
    app.register_blueprint(bp_book_release)
