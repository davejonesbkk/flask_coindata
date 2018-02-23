
"""

1 - Get prices for X coins and save to database
2 - Pull data for coins from database
3 - Run everyhour to get latest price and append to previous price
4 - Render in templates

"""

import json, urllib.request


class CoinData:

	def get_coins(self, coin):

		coins = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'ADA', 'XLM', 'NEO', 'IOTA', 'DASH' ]

		base_url = 'https://min-api.cryptocompare.com/data/price?fsym='
		connector = '&tsyms='

		fiat = 'USD'

		for coin in coins:
			endpoint = base_url+coin+connector+fiat

			return endpoint

		with urllib.request.urlopen(endpoint) as url:
			data = json.loads(url.read().decode())
		return data





