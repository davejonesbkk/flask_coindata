from ac_data import app

if __name__ == '__main__':
	"""use_reloader needed when using apscheduler to prevent
	flask starting two processes"""
	app.run(use_reloader=False) 