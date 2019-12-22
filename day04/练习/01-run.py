import os
from flask import Flask, request, render_template
import datetime

app = Flask(__name__)

@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('02-upload.html')
    else:
        uname = request.form.get('uname')
        f = request.files['uimg']
        # 获取时间字符串
        ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        # 获取文件的后缀名
        ext = f.filename.split('.')[1]
        filename = ftime+'.'+ext
        text = "用户名为 "+ uname +" 在 "+ ftime +" 上传了图片！"
        print(text)
        # 拼目录
        basedir = os.path.dirname(__file__)
        upload_path = os.path.join(basedir, 'static/upload', filename)
        print(upload_path)
        f.save(upload_path)
        return "Upload Success"

if __name__ == '__main__':
    app.run(debug=True)
