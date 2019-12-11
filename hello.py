from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
from sqlalchemy import func, desc
import pymysql
import json   #转换成Json格式的程序
import numpy as np
import decimal

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mbitadmin@localhost:3306/flask"
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# 数据字典
# plan_price_ranges表的数据结构
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

class DateEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime(DATETIME)
        elif isinstance(obj,datetime.date):
            return obj.strftime(DATE)
        elif isinstance(obj,Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self,obj)

def queryToDict(models):
    if(isinstance(models,list)):
        if(isinstance(models[0],Model)):
            lst = []
            for model in models:
                gen = model_to_dict(model)
                dit = dict((g[0],g[1]) for g in gen)
                lst.append(dit)
            return lst
        else:
            res = result_to_dict(models)
            return res
    else:
        if (isinstance(models, Model)):
            gen = model_to_dict(models)
            dit = dict((g[0],g[1]) for g in gen)
            return dit
        else:
            res = dict(zip(models.keys(), models))
            find_datetime(res)
            return res
#当结果为result对象列表时，result有key()方法
def result_to_dict(results):
    res = [dict(zip(r.keys(), r)) for r in results]
    #这里r为一个字典，对象传递直接改变字典属性
    for r in res:
        find_datetime(r)
    return res
def model_to_dict(model):      #这段来自于参考资源
    for col in model.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(model, col.name))
        elif isinstance(col.type, Numeric):
            value = float(getattr(model, col.name))
        else:
            value = getattr(model, col.name)
        yield (col.name, value)
def find_datetime(value):
    for v in value:
        if (isinstance(value[v], cdatetime)):
            value[v] = convert_datetime(value[v])   #这里原理类似，修改的字典对象，不用返回即可修改
def convert_datetime(value):
    if value:
        if(isinstance(value,(cdatetime,DateTime))):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif(isinstance(value,(date,Date))):
            return value.strftime("%Y-%m-%d")
        elif(isinstance(value,(Time,time))):
            return value.strftime("%H:%M:%S")
    else:
        return ""   
#显示所有数据
@app.route('/')
def show_all():
   return render_template('show_all.html', plan_price_ranges1 = plan_price_ranges.query.all() )

#新增数据
@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['store'] or not request.form['gender'] or not request.form['pclass']:
         flash('Please enter all the fields', 'error')
      else:
         plan_price_range = plan_price_ranges(request.form['store'], request.form['gender'],
            request.form['pclass'], request.form['price'], request.form['year'],
            request.form['month'], request.form['unit'])
         
         db.session.add(plan_price_range)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

#获取plan_price_ranges表中的数据，转换为json格式
@app.route('/comments', methods=['GET'])
def comments():
    plan_price_ranges1 =  plan_price_ranges.query.all()
    result = []
    for plan_price_range in plan_price_ranges1:
        result.append(plan_price_range.to_json())
    return jsonify({'rows': result})
    #return render_template('plan_price_range.html', result_json = jsonify({'row': result}))

@app.route('/get_category_sum', methods=['GET'])
def get_category_sum():
    UnReadMsg = db.session.query(plan_price_ranges.pclass, func.sum(plan_price_ranges.unit).label("销售数量")).group_by(plan_price_ranges.pclass).all()
    return result_to_dict(UnReadMsg)
        
#获取全部数据的分类汇总透视表
@app.route('/newppr', methods=['GET'])
def newppr():
    return render_template('plan_price_range.html')

#主从数据表
@app.route('/layered', methods=['GET'])
def layered():
    return render_template('layered_tbls.html')
    
@app.route('/interactive')
def interactive():
	return render_template('interactive.html')
	
if __name__ == '__main__':
   db.create_all()
   app.run(host='0.0.0.0',debug = True)
