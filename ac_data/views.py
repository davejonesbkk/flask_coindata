import sqlite3, os, urllib, json, time

from flask import render_template, request, redirect, url_for, g 

from ac_data import app 

from .models import connect_db, init_db, get_db, close_db

#from .scheduler import run_prices



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

	coindata = []

	db = get_db()

	for coin in coins:
		endpoint = base_url+coin+connector+fiat


		with urllib.request.urlopen(endpoint) as url:
			data = json.loads(url.read().decode())
			print(data)
			
			for k,v in data.items():
					price = v
					coindata.append((coin,v))

		db.executemany('insert into prices (coin, usd) values (?, ?)', (coindata))

	db.commit()

	return render_template('coindata.html', coindata=coindata)




