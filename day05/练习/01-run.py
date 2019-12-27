from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import pymysql
from sqlalchemy import or_

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:horsin@123@localhost:3306/flask"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

# 根据现有的表结构构建模型类
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(80),unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120),unique=True)

    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email

    def __repr__(self):
        return "<Users:%s>" % self.username

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cname = db.Column(db.String(80))

    def __init__(self, cname):
        self.cname = cname

    def __repr__(self):
        return "<Course:%s>" % self.cname

db.create_all()

@app.route('/insert', methods=['GET', 'POST'])
def insert_views():
    if request.method == 'POST':
        user = Users("horsin", '24', "1915887870@qq.com")
        db.session.add(user)
        db.session.commit()
        return "Insert OK"
    else:
        return "Insert Failed"

@app.route('/query')
def query_views():
    # 测试查询
    # print(db.session.query(Users))
    # print(db.session.query(Users.username, Users.email))
    # print(db.session.query(Users, Course))

    # 通过查询执行函数获得最终查询结果
    # all() : 得到查询中的所有结果
    # users = db.session.query(Users).all()
    # for u in users:
    #     print(u.username, u.age, u.email)

    # first() : 得到查询的第一个结果
    # user = db.session.query(Users).first()
    # print(user.username, user.age, user.email)
    # count() : 得到查询结果的数量
    # num = db.session.query(Users).count()
    # print(num)

    # 使用查询过滤器函数对数据进行筛选
    # users = db.session.query(Users).filter(Users.age > 30).all()
    # users = db.session.query(Users).filter(Users.age > 30, Users.id >= 1).all()
    # users = db.session.query(Users).filter(or_(Users.age > 30, Users.id < 1)).all()
    # users = db.session.query(Users).filter(Users.id == 1).first()
    # users = db.session.query(Users).filter(Users.email.like('%z%')).all()
    # users = db.session.query(Users).filter(Users.id.in_([1, 2, 3])).all()

    # filter_by()
    # users = db.session.query(Users).filter_by(id=1).first()

    # limit()
    # users = db.session.query(Users).limit(5).all()
    # users = db.session.query(Users).limit(5).offset(1).all()

    # order_by()
    # users = db.session.query(Users).order_by('id desc').all()

    # group_by()
    # users = db.session.query(Users.age).group_by('age').all()

    # 基于 Models 实现的查询:查询 id > 3 的所有用户的信息
    users = Users.query.filter(Users.id > 1).all()
    print(users)
    return "Query OK"

@app.route('/delete_user')
def delete_user():
    user = Users.query.filter_by(id = 5).first()
    db.session.delete(user)
    return "Delete OK"

@app.route('/update_user')
def update_user():
    user = Users.query.filter_by(id=1).first()
    user.username = "linhorsin"
    user.age = 24
    db.session.add(user)
    return "Update OK"

if __name__ == '__main__':
    app.run(debug=True)