from functools import wraps
from flask import redirect, url_for, flash, session

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("You don't have permission to access this page.", 'danger')
            return redirect(url_for('routes.forbidden'))
        return f(*args, **kwargs)
    return decorated_function
