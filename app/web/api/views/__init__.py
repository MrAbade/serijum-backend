def configure(app):
    from .user import bp_user
    app.register_blueprint(bp_user)

    from .suite import bp_suite
    app.register_blueprint(bp_suite)

    from .schedule import bp_schedule
    app.register_blueprint(bp_schedule)

    from .isbusy import bp_isbusy
    app.register_blueprint(bp_isbusy)

    from .category import bp_category
    app.register_blueprint(bp_category)
