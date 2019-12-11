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

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)    # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:    # 添加了对datetime的处理
                    print(type(data),data)
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] # SQLserver数据库中毫秒是3位，日期格式;2015-05-12 11:13:58.543
                    elif isinstance(data, datetime.date):
                        fields[field] = datadata.strftime("%Y-%m-%d")
                    elif isinstance(data, decimal.Decimal):
                        fields[field]= float(data)
                        #return float(data)
                    else:
                        fields[field] = AlchemyEncoder.default(self, data) # 如果是自定义类，递归调用解析JSON，这个是对象映射关系表 也加入到JSON
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)
 
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            data = str(obj, encoding='utf-8')
        if isinstance(obj, decimal.Decimal):
            data = int(obj)
        return dict(data)
   
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
    msgs = []
    for msg in UnReadMsg:
        msgs.append(msg)
    rts = json.dumps(msgs, cls=MyEncoder,ensure_ascii=False)
    #rts = jsonify(JSONHelper.jsonBQlist(msgs))
    return rts
        
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
