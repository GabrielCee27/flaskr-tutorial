import sqlite3
import click

# g is a special object that's unique for each request;
# It's used to store data that might be accessed by multiple functions during the request.
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # tells the connection to return rows that behave like dicts
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    # points to the Flask application handling the request
    # b/c we used an application factory
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# defines the command line 'init-db'
# to call the init_db function
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    # to call close_db when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with the flask command
    app.cli.add_command(init_db_command)
