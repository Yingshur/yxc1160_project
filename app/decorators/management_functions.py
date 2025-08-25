from flask_login import current_user
from functools import wraps
from flask import abort
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if current_user.role != "Admin":
                return abort(403)
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return abort(403)

    return wrapper
