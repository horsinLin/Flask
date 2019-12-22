from flask import Flask, render_template, request, make_response

app = Flask(__name__,template_folder='templates',static_url_path='/s',static_folder='s')

@app.route('/')
def index():
    return render_template('01-index.html')

@app.route('/request')
def request_views():
    # 将 request 中的成员打印在终端上
    # print(dir(request))
    # 获取请求方案(协议)
    scheme = request.scheme
    # 获取请求方式
    method = request.method
    # 获取get请求方式提交的数据
    args = request.args
    # 获取post请求方式提交的数据
    form = request.form
    # 获取任意一种请求方式提交的数据
    values = request.values
    # 获取cookies中的信息
    cookies = request.cookies
    # 获取请求消息头信息
    headers = request.headers
    # 获取请求url地址
    path = request.path
    # 获取用户上传文件
    files = request.files
    # 获取headers中的User-Agent请求消息头
    ua = headers['User-Agent']
    # 获取headers中的referer请求消息头：请求的源地址
    ref = request.headers.get('referer','')
    return render_template('02-request.html',params=locals())

@app.route('/form')
def form_views():
    return render_template('03-form.html')

@app.route('/form_do')
def form_do():
    if request.method == 'GET':
        # 获取 form 表单提交过来的数据
        uname = request.args.get('uname')
        upwd = request.args.get('upwd')
        return "用户名称：%s,用户密码：%s"%(uname,upwd)

@app.route('/post')
def post_views():
    return render_template('04-form.html')

@app.route('/post_do',methods=['POST'])
def post_do():
    if request.method == "POST":
        uname = request.form.get('uname')
        upwd = request.form.get('upwd')
        uemail = request.form.get('uemail')
        utname = request.form.get('utname')
        text = "用户名：%s，密码：%s，邮箱：%s，真实姓名：%s"\
               % (uname,upwd,uemail,utname)
        print(text)
    return text

@app.route('/response')
def response_views():
    # 响应普通字符串给客户端 - 使用响应对象
    # 创建响应对象，并赋值响应的字符串
    # resp = make_response('使用响应对象响应回去的内容')
    # 创建响应对象，并赋值响应的模板
    resp = make_response(render_template('01-index.html'))
    # 将响应对象返回
    return resp

@app.route('/file', methods=['GET','POST'])
def file_views():
    if request.method == 'GET':
        return render_template('05-file.html')
    else:
        # 接收名称为 uimg 的图片(文件)
        f = request.files['uimg']
        # 获取上传的图片的名称
        filename = f.filename
        print('文件名称：' + filename)
        # 再讲图片保持进 static 目录中
        f.save('s/img/' + filename)
        return "Upload OK"

if __name__ == '__main__':
    app.run(debug=True)