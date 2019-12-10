from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import getjson   #转换成Json格式的程序

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mbitadmin@localhost:3306/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class plan_price_ranges(db.Model):
	id = db.Column('id', db.Integer, primary_key = True)
	store = db.Column(db.String(50))
	gender = db.Column(db.String(10))
	pclass = db.Column(db.String(100))
	price = db.Column(db.Integer) 
	year=db.Column(db.Integer) 
	month=db.Column(db.Integer) 
	unit = db.Column(db.Integer)

	def __init__(self, store,gender, pclass, price,year,month,unit):
		self.store = store
		self.gender = gender
		self.pclass = pclass
		self.price = price
		self.year = year
		self.month = month
		self.unit = unit
	
	def to_json(self):
		dict = self.__dict__
		if "_sa_instance_state" in dict:
			del dict["_sa_instance_state"]
		return dict

plan_price_ranges1 =  plan_price_ranges.query.all()
result = []
for plan_price_range in plan_price_ranges1:
    result.append(plan_price_range.to_json())
print(result)
