import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# A blueprint is a set of operations that can be registered on an application
# creates a blueprint named 'auth'
# __name__ lets the blueprint know where it's defined
# the url prefix will be prepended to all the URLs associated
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # Start validating the input
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # checking for invalidation
        if not username: # if username is None
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif db.execute('SELECT id FROM user WHERE username = ?',
        (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password)))
            db.commit() # saves the changes
            # registerd, now they can log in
            return redirect(url_for('auth.login'))

        # stores messages that can be retrieved when rendering the template
        flash(error)

    # Refreshes the same page
    return render_template('auth/register.html')

@bp.route('login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('logout')
def logout():
    session.clear()
    return (redirect(url_for('index')))

# going to be used as a decorator to check before calling a view
def login_required(view):
    # functool.wraps takes a function used in a decorator and adds the
    # functionality of copying over the function name, docstring,
    # arguments list, etc.
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
