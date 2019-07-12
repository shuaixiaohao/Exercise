from functools import wraps

from flask import session, url_for, redirect


def is_login(func):
    @wraps(func)
    def check_login():
        result = session.get('user_id')
        if result:
            return func()
        else:
            return redirect(url_for('user.login'))
    return check_login
