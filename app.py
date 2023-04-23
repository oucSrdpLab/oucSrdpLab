from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from pymysql import IntegrityError

app = Flask(__name__)

app.config['STATIC_FOLDER']='static'
app.template_folder = 'templates'
app.config['STATIC_URL_PATH']='/static'

HOSTNAME="localhost"
PORT=3306
USERNAME="root"
PASSWORD="20230421"
DATABASE="welab"

app.config['SQLALCHEMY_DATABASE_URI']=f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
#app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:129238905ad@110.41.20.227:3306/welab"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True

db=SQLAlchemy(app)

class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)#nullable指是否可以为空
    number=db.Column(db.String(100),nullable=False)
    identification=db.Column(db.String(100),nullable=False)

class Orders(db.Model):
    __tablename__="orders"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    itemName=db.Column(db.String(100),nullable=False)
    itemPlace=db.Column(db.String(100),nullable=False)
    applicantName=db.Column(db.String(100),nullable=False)
    applicantIDNumber=db.Column(db.String(100),nullable=False)
    managerName=db.Column(db.String(100),nullable=False)
    startTime=db.Column(db.String(100),nullable=False)
    untilTime=db.Column(db.String(100),nullable=False)
    itemID=db.Column(db.String(100),nullable=False)
    orderStatus=db.Column(db.String(100),nullable=False)
    ifChecked=db.Column(db.String(100),nullable=False)
    reserveReason=db.Column(db.String(100),nullable=False)
    attendance=db.Column(db.String(100),nullable=False)
    sortId=db.Column(db.String(100),nullable=False)

class Lab(db.Model):
    __tablename__ = "lab"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manager = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # nullable指是否可以为空
    academy = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    usage = db.Column(db.String(100), nullable=False)

class Equipment(db.Model):
    __tablename__ = "equipment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manager = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # nullable指是否可以为空
    academy = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    usage = db.Column(db.String(100), nullable=False)

class Info(db.Model):
    __tablename__ = "info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identification = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # nullable指是否可以为空
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    kind = db.Column(db.String(100), nullable=False)
    contact=db.Column(db.String(100), nullable=False)

class Feedback(db.Model):
    __tablename__="feedback"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.String(100),nullable=False)#nullable指是否可以为空
    identification=db.Column(db.String(100),nullable=False)
    name=db.Column(db.String(100),nullable=False)

with app.app_context():
    db.create_all()#将表映射到数据库中

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")

#注册
@app.route('/database/register',methods=['POST','GET'])
def user_add():
    req_data = request.get_json()
    userName = req_data.get('name')
    passWord=req_data.get('password')
    Number=req_data.get('number')
    user=User(username=userName, password=passWord, number=Number, identification="student")
    db.session.add(user)
    db.session.commit()
    data = {
        "username": userName,
        "password": passWord,
        "number": Number
    }
    return data

#订单
@app.route('/database/orders',methods=['POST','GET'])
def orders_add():
    res = request.get_json()
    op = res.get('op')
    #op为操作码，1为写入order
    if op == 1:
        order = res.get('order')
        iN = order.get('itemName')
        iP = order.get('itemPlace')
        aN = order.get('applicantName')
        reserveReason=res.get('reserveReason')
        aID = order.get('applicantIDNumber')
        mN = order.get('managerName')
        sT = order.get('startTime')
        uT = order.get('untilTime')
        iT = order.get('itemID')
        sortId = res.get('sortId')
        orders = Orders(itemName=iN, itemPlace=iP, applicantName=aN, applicantIDNumber=aID,
                        managerName=mN, startTime=sT, untilTime=uT, itemID=iT, reserveReason=reserveReason,
                        sortId=sortId, orderStatus="1", ifChecked="true", attendance="false")
        db.session.add(orders)
        db.session.commit()
        data = {
            "itemName": iN,
            "itemPlace": iP,
            "applicantName": aN
        }
        return data
    #2为读操作
    elif op == 2:
        order = Orders.query.all()
        order_list = [{'startTime': order.startTime, 'untilTime': order.untilTime, '_id': order.id,'ifChecked':order.ifChecked,'reserveReason':order.reseveReason} for order in orders]
        return jsonify(order_list)
    #3为删除
    elif op == 3:
        order_id = res.get('id')
        order = Orders.query.get(order_id)
        if not order:
            return jsonify({'msg': 'Order not found'})
        db.session.delete(order)
        db.session.commit()
        return jsonify({'msg': 'Order deleted successfully'})
    else:
        return jsonify({'msg': 'Invalid action'})

#实验室接口
@app.route('/database/lab',methods=['POST','GET'])
def lab_add():
    res=request.get_json()
    op=res.get('op')
    #1为写
    if op == 1:
        m = res.get('manager')
        n = res.get('name')
        a = res.get('academy')
        p = res.get('place')
        u = res.get('usage')
        lab = Lab(manager=m, name=n, academy=a, place=p, usage=u)
        db.session.add(lab)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'msg': 'Order already exists'})
        return jsonify({'msg': 'Order created successfully'})
    #2为读
    if op == 2:
        order = Lab.query.all()
        order_list = [
            {'academy': order.academy, 'usage': order.usage, 'place': order.place, 'manager': order.manager,
             'name': order.name} for order in order]
        return jsonify(order_list)

#信息
@app.route('/database/info',methods=['POST','GET'])
def info_add():
    res = request.get_json()
    op = res.get('op')
    #1为写
    if op == 1:
        info = Info(name="test", identification="test", title="test", content="test", kind="test", contact="test")
        db.session.add(info)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'msg': 'Order already exists'})
        return jsonify({'msg': 'Order created successfully'})
    #2 read
    elif op == 2:
        order = Info.query.all()
        order_list = [
            {'title': order.title, 'content': order.content, 'name': order.name, 'identification': order.identification,
             'kind': order.kind,'contact':order.contact} for order in orders]
        return jsonify(order_list)
    #3 delete
    elif op == 3:
        order_id = res.get('id')
        order = Info.query.get(order_id)
        if not order:
            return jsonify({'msg': 'Order not found'})
        db.session.delete(order)
        db.session.commit()
        return jsonify({'msg': 'Order deleted successfully'})


@app.route('/database/feedback',methods=['POST','GET'])
def feedback():
    res = request.get_json()
    op = res.get('op')
    # 1为写
    if op == 1:
        t = res.get('title')
        c = res.get('content')
        i = res.get('identification')
        n = res.get('name')
        feedback = Feedback(title=t, content=c, identification=i, name=n)
        db.session.add(feedback)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'msg': 'Order already exists'})
        return jsonify({'msg': 'Order created successfully'})
    # 2为读
    if op == 2:
        order = Feedback.query.all()
        order_list = [
            {'title': order.title, 'content': order.content, 'name': order.name, 'identification': order.identification} for order in orders]
        return jsonify(order_list)


@app.route('/database/equipment',methods=['POST','GET'])
def equipment():
    res = request.get_json()
    op = res.get('op')
    # 1为写
    if op == 1:
        m = res.get('manager')
        n = res.get('name')
        a = res.get('academy')
        p = res.get('place')
        u = res.get('usage')
        equipment = Equipment(manager=m, name=n, academy=a, place=p, usage=u)
        db.session.add(equipment)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'msg': 'Order already exists'})
        return jsonify({'msg': 'Order created successfully'})
    # 2为读
    if op == 2:
        order = Equipment.query.all()
        order_list = [
            {'academy': order.academy, 'usage': order.usage, 'place': order.place, 'manager': order.manager,
             'name': order.name} for order in order]
        return jsonify(order_list)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
