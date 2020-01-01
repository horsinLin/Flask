from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/set_cookie')
def set_cookie():
    # 将响应内容构建成响应对象
    resp = make_response("Set Cookies Success")
    # 保存数据到cookie
    resp.set_cookie('username', 'sf.zh')
    # 保存数据到cookie并设置max_age
    resp.set_cookie('keywords', 'Cannon', max_age=3600)
    return resp

@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    keywords = request.cookies.get('keywords')
    print('username:%s,keywords:%s' % (username, keywords))
    return "Get Cookies Success"

if __name__ == '__main__':
    app.run()