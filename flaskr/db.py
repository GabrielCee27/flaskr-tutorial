import sqlite3
import click

# g is a special object that's unique for each request.
# It's used to store data that might be accessed by multiple functions during the request.
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        # have to make a new db connection
        g.db = sqlite3.connect(
            current_app.config['DATABASE']
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db # just returns existing db if available

def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read.decode('utf8'))

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
    # adds a new command that can be calles with the flask command
    app.cli.add_command(init_db_command)
