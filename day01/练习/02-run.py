from flask import Flask

app = Flask(__name__)

# 主页
@app.route('/')
def index():
	return "主页"
# 登录
@app.route('/login')
def login():
	return "登录界面"
# 注册
@app.route('/register')
def register():
	return "注册界面"

@app.route('/show1/<name>')
def show1(name):
	return "<h1>姓名为：%s</h1>" % name

if __name__ == '__main__':
    app.run(debug=True)