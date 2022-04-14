from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

#instantiate an object of Flask
app = Flask(__name__,instance_relative_config=True)
csrf=CSRFProtect(app)

from carsapp import config
app.config.from_object(config.ProductionConfig)
app.config.from_pyfile('config.py',silent=False)

db =SQLAlchemy(app)

#load your routes here

from carsapp.myroutes import adminroutes,userroutes
from carsapp import forms
from carsapp import models

#load he config
