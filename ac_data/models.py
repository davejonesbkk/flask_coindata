
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

from datetime import datetime

from ac_data import app 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/coindatatest.db'
db = SQLAlchemy(app)

class Coin(db.Model):
	name = db.Column(db.String, primary_key = True)

	def __repr__(self):
		return '<Coin name %r>' % self.name 

class Price(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Integer, nullable=False)
	datetime = db.Column(db.DateTime, nullable=False,
		default=datetime.utcnow)

	coin_name = db.Column(db.String, db.ForeignKey('coin.name'),
		nullable=False)

	coin = db.relationship('Coin',
		backref=db.backref('prices'))

	def __repr__(self):
		return ('<Price of %s is %d>' % (self.coin_name, self.price))


	


