from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:horsin@123@localhost:3306/flask"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

# 根据Users表结构设计Users类
class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(80),unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120),unique=True)

    def __init__(self,username,age,email):
        self.username = username
        self.age = age
        self.email = email

    def __repr__(self):
        return "<Users:%s>" % self.username

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cname = db.Column(db.String(80))
    # 反向引用:返回与当前课程相关的teacher列表
    # backref:定义反向关系,本质上会向Teacher实体中增加一个course属性,
    # 该属性可替代course_id来访问Course模型,此时会得到的是模型对象,而不是外键值
    teachers = db.relationship('Teacher', backref='course')

    def __init__(self, cname):
        self.cname = cname

    def __repr__(self):
        return "<Course:%s>" % self.cname

class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tname = db.Column(db.String(30))
    tage = db.Column(db.Integer)
    # 增加一列:course_id,外键列,要引用自主键表(course)的主键列(id)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __init__(self, tname, tage):
        self.tname = tname
        self.tage = tage

    def __repr__(self):
        return "<Teacher:%s>" % self.tname

db.drop_all()
db.create_all()

@app.route('/query_all')
def query_all():
    users = db.session.query(Users).all()
    return render_template('01-users.html',params=locals())

# @app.route('/query_by_id/<int:id>')
# def query_by_id(id):
#     user = db.session.query(Users).filter_by(id=id).first()
#     return render_template('02-users.html',params=locals())

@app.route('/query_by_id')
def query_by_id():
    id = request.args.get('id')
    user = db.session.query(Users).filter_by(id=id).first()
    return render_template('02-users.html',params=locals())

@app.route('/delete')
def delete_view():
    # 接收请求过来的 id 值
    id = request.args.get('id')
    # 根据id值查询出对应的模型对象
    user = Users.query.filter_by(id=id).first()
    # 将模型对象删除
    db.session.delete(user)
    url = request.headers.get('referer', '/query_all')
    return redirect(url)

@app.route('/update', methods=['GET', 'POST'])
def update_view():
    if request.method == 'GET':
        id = request.args.get('id')
        user = Users.query.filter_by(id=id).first()
        return render_template('03-update.html', params=locals())
    else:
        id = request.form.get('id')
        username = request.form.get('username')
        age = request.form.get('age')
        email = request.form.get('email')

        user = Users.query.filter_by(id=id).first()

        user.username = username
        user.age = age
        user.email = email

        db.session.add(user)
        return redirect('/query_all')

@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'GET':
        return render_template('03-users.html')
    else:
        name = request.form.get('uname')
        age = request.form.get('uage')
        email = request.form.get('uemail')
        user = Users(name, age, email)
        db.session.add(user)
        db.session.commit()
        return redirect('/query_all')

if __name__ == '__main__':
    app.run(debug=True)