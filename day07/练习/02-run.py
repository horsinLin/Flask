from flask import Flask, request, render_template, make_response, session
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:horsin@123@localhost:3306/flask"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SECRET_KEY'] = "INPUT A STRING"

db = SQLAlchemy(app)

# 创建用户表
class loginUser(db.Model):
    __tablename__ = 'loginUser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True)
    passwd = db.Column(db.String(120))

    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd

    def __repr__(self):
        return "<loginUser : %r>" % self.username

db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register_views():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = loginUser(username, password)
        db.session.add(user)
        return "Register OK"


@app.route('/login', methods=['POST', 'GET'])
def login_view():
    if request.method == 'GET':
        # 判断之前是否有成功登录(id和uname是否存在与cookie上)
        if 'id' in request.cookies and 'username' in request.cookies:
            return "您已成功登录"
        else:
            return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        rem = request.form.get('remberPass')
        user = loginUser.query.filter_by(username=username, passwd=password).first()
        if user:
            resp = make_response("login OK")
            if rem == "on":
                resp.set_cookie('id', str(user.id), max_age=3600)
                resp.set_cookie('username', user.username, max_age=3600)
            return resp
        else:
            return "login Failed"

@app.route('/set_session')
def setSession():
    session['username'] = 'sanfeng.zhang'
    return "Set session Success"

@app.route('/get_session')
def getSession():
    username = session['username']
    print(username)
    return "Get session Success"

@app.route('/del_session')
def delSession():
    del session['username']
    return "Delete Session Success"

@app.route('/create_xhr')
def create_xhr():
    return render_template('xhr.html')

if __name__ == '__main__':
    app.run(debug=True)