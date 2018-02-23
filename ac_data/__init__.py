from flask import Flask 
app = Flask(__name__)

import ac_data.views

app.config.from_object('config')

