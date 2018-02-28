import sqlite3, os, urllib, json, time

from flask import render_template, request, redirect, url_for, g 

from ac_data import app 

from .models import connect_db, init_db, get_db, close_db

from .scheduler import initialize, get_coin_data



@app.route('/')
def index():

	db = get_db()
	cur = db.execute('select coin, usd from prices order by id desc')
	prices = cur.fetchall()


	return render_template('index.html', prices=prices)

@app.route('/coindata')
def coindata():

	
	get_coin_data()

	return render_template('coindata.html', coindata=coindata)




