from functools import wraps
from flask import session, redirect, url_for, abort

def requires_login(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('auth.login_google'))
        return view_func(*args, **kwargs)
    return wrapped_view

def requires_role(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            user_role = session.get("user_role")
            if user_role != role:
                return abort(403, description="Access denied")
            return view_func(*args, **kwargs)
        return wrapped_view
    return decorator
