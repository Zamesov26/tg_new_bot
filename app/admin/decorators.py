from functools import wraps


class NotAdminError(Exception):
    pass


def only_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get("user") == "admin":
            return func(*args, **kwargs)
        raise NotAdminError

    return wrapper
