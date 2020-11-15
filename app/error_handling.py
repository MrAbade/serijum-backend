class UnauthorizedUser(Exception):
    def __init__(self, *args, **kwargs):
        super(UnauthorizedUser, self).__init__(*args, **kwargs)


class IdWasNotFound(Exception):
    def __init__(self, *args, **kwargs):
        super(IdWasNotFound, self).__init__(*args, **kwargs)
