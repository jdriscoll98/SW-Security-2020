import sqlite3
import click
from flask import Flask, render_template, g, request
from flask.cli import with_appcontext

app = Flask(__name__)


#####################
#Database connection#
#####################

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('./database.db')
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

############
#Page Views#
############

init_app(app)

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('language')
        password = request.form.get('password')

    return render_template('create_account.html')
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')