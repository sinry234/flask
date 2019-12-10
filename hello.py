from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json   #转换成Json格式的程序

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
		rs = db.session.query(plan_price_ranges.store,plan_price_ranges.gender,plan_price_ranges.pclass, db.func.sum(plan_price_ranges.unit)).group_by(plan_price_ranges.store,plan_price_ranges.gender,plan_price_ranges.pclass).all()
    result1 = []
    for line in rs:
        result1.append(line.to_json())
    return jsonify({'rows': result1})
        
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
