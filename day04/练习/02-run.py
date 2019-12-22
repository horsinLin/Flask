from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://root:horsin@123@localhost:3306/flask'

db = SQLAlchemy(app)

# 创建模型类 - Models
# 创建 Users 类,映射到表中叫 users 表
# 创建字段: id,主键,自增
# 创建字段: username,长度为80的字符串,不允许为空,必须唯一
# 创建字段:age,整数,允许为空
# 创建字段:email,长度为120的字符串,必须唯一
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, usename, age, email):
        self.username = usename
        self.age = age
        self.email = email

    def __repr__(self):
        return '<Users:%r>' % self.username

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sname = db.Column(db.String(30), nullable=False)
    sage = db.Column(db.Integer)

    def __init__(self, sname, sage):
        self.sname = sname
        self.sage = sage

    def __repr__(self):
        return "<Student:%r>" % self.sname

class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tname = db.Column(db.String(30), nullable=False)
    tage = db.Column(db.Integer)

    def __init__(self, tname, tage):
        self.tname = tname
        self.tage = tage

    def __repr__(self):
        return "<Teacher:%r>" % self.tname

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cname = db.Column(db.String(30))

    def __init__(self, cname):
        self.cname = cname

    def __repr__(self):
        return "<Course:%r>" % self.cname

# 将创建好的实体类映射回数据库
db.create_all()

@app.route('/insert')
def insert_views():
    # 创建 Users 对象
    users = Users('张三丰',38,'zsf@qq.com')
    # 将对象通过 db.session.add() 插入到数据库
    db.session.add(users)
    # 提交插入操作
    db.session.commit()
    return "Insert Success"

@app.route('/register', methods=['GET','POST'])
def register_views():
    if request.method == 'GET':
        return render_template('03-users.html')
    else:
        uname = request.form.get('uname')
        uage = request.form.get('uage')
        uemail = request.form.get('uemail')

        # 创建 Users 对象
        users = Users(uname, uage, uemail)
        # 将对象通过 db.session.add() 插入到数据库
        db.session.add(users)
        # 提交插入操作
        db.session.commit()

        return "添加用户: %s 成功!" % (uname)

if __name__ == '__main__':
    app.run(debug=True)