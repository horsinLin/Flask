from flask import Flask, url_for

app = Flask(__name__)

@app.route('/post',methods=['GET'])
def post():
    return "这是post请求方式进来的"

@app.route('/login')
def login():
    return "登陆"

@app.route('/show1/<name>')
def show1(name):
	return "<h1>姓名为：%s</h1>" % name

@app.route('/url')
def url_views():
    # 将login()反向解析访问地址
    # logUrl = url_for('login')
    # print(logUrl)
    #
    # resp = "<a href='"+logUrl+"'>我要登陆</a>"
    # return resp
    url = url_for('show1',name="horsin")
    print(url)
    resp = "<a href='"+url+"'>我要登陆</a>"
    return resp

if __name__ == '__main__':
    app.run(debug=True)