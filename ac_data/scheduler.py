
import sqlite3, os, urllib, json, time, urllib.request, atexit

from ac_data import app

from .models import connect_db, init_db, get_db, close_db

from apscheduler.schedulers.background import BackgroundScheduler 
from apscheduler.triggers.interval import IntervalTrigger 

@app.before_first_request
def initialize():
	scheduler = BackgroundScheduler()
	scheduler.start()
	scheduler.add_job(
		func=get_coin_data,
		trigger=IntervalTrigger(seconds=100),
		id='printing_job',
		name='Get current USD price of all coins in list',
		replace_existing=True)
	#Shutdown the scheduler when the app exits
	atexit.register(lambda: scheduler.shutdown())

def get_coin_data():
	with app.app_context():
		print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

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
				#print(data)
				
				for k,v in data.items():
						price = v
						coindata.append((coin,v))


		db.executemany('insert into prices (coin, usd) values (?, ?)', (coindata))

		db.commit()

		#print(coindata)

		return(coindata)





