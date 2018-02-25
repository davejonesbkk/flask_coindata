import sqlite3, os

from ac_data import app

from flask import g 

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'coindata.db'),
	SECRET_KEY='FuSNU+aa/OTCzmkyYCJsOvrUnacSalu5XTZ7tQp+gU7Ar0giKy',
	USERNAME='admin',
	PASSWORD='default'
))

app.config.from_envvar('AC_DATA_SETTINGS', silent=True)

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row 
	return rv 

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('Initialized the database')

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db=connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()