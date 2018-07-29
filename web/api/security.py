from functools import wraps

def requires_auth(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        # TODO validate authentication (return 401 if fails)
        return func(*args, **kwargs)
    return decorator
