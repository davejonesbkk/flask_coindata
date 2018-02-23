import sqlite3, os, urllib, json

from flask import render_template, request, redirect, url_for, g 

from ac_data import app 


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

@app.route('/')
def index():

	db = get_db()
	cur = db.execute('select coin, usd from prices order by id desc')
	prices = cur.fetchall()


	return render_template('index.html', prices=prices)

@app.route('/coindata')
def coindata():

	coins = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'ADA', 'XLM', 'NEO', 'IOTA', 'DASH' ]

	base_url = 'https://min-api.cryptocompare.com/data/price?fsym='
	connector = '&tsyms='

	fiat = 'USD'

	coindata = {}

	db = get_db()

	for coin in coins:
		endpoint = base_url+coin+connector+fiat


		with urllib.request.urlopen(endpoint) as url:
			data = json.loads(url.read().decode())
			for k,v in data.items():
					price = v

			coindata.update({coin:v})

	db.execute('insert into prices (coin, usd) values (?, ?)',
		coin, price)

	
	
	print(coindata)


	#db.executemany('insert into prices (coin, usd) values (?, ?)', (coindata,))

	db.commit()

	db.close()

	return render_template('coindata.html', coindata=coindata)




