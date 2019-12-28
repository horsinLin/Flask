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
    teachers = db.relationship('Teacher', backref='course', lazy='dynamic')

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

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sname = db.Column(db.String(30))
    # 增加关联属性以及反向引用
    courses = db.relationship(
        'Course',
        secondary='student_course',
        lazy='dynamic',
        backref=db.backref('students',lazy='dynamic')
    )

    def __init__(self, sname):
        self.sname = sname

    def __repr__(self):
        return "<Student : %r>" % self.sname

student_course = db.Table(
    'student_course',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
)

# db.drop_all()
db.create_all()

@app.route('/add_course')
def add_course():
    course1 = Course('PYTHON 基础')
    course2 = Course('PYTHON 高级')
    course3 = Course('PYTHON Web 基础')
    course4 = Course('PYTHON Web 开发')
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(course4)
    return "add course ok"

@app.route('/add_teacher')
def add_teacher():
    teacher = Teacher('魏老师', 35)
    # teacher.course_id = 1
    # 根据 course_id 查询出一个 Course 实体,再将Course实体赋值给teacher
    course = Course.query.filter_by(id=1).first()
    teacher.course = course
    db.session.add(teacher)
    return "Add teacher OK"

@app.route('/addTeacher', methods=['GET', 'POST'])
def addTeacher():
    if request.method == 'GET':
        course = Course.query.filter().all()
        return render_template('01-addTeacher.html', params=locals())
    else:
        tname = request.form.get('username')
        tage = request.form.get('age')
        course_id = request.form.get('course_id')
        course = Course.query.filter_by(id=course_id).first()
        teacher = Teacher(tname, tage)
        teacher.course = course
        db.session.add(teacher)
        return redirect('/course_info')

@app.route('/query_teacher')
def query_teacher():
    # 通过 course 查询对应所有的 teacher
    # 查询 id 为 1 的 course 对象
    # course = Course.query.filter_by(id=1).first()
    # 根据 course 对象查询所有的 teacher 对象
    # teachers = course.teachers.all()
    # print(teachers)

    # 通过 teacher 查询 course
    teacher = Teacher.query.filter_by(tname='张三丰').first()
    course = teacher.course
    print("老师:%s, 课程:%s" % (teacher.tname, course.cname))
    return "Query OK"

@app.route('/course_info')
def course_info():
    teachers = Teacher.query.all()
    return render_template('02-course.html', params=locals())

# 向多对多的关联表中增加数据
@app.route('/add_student_course')
def add_student_course():
    # 查询张飞的信息
    stu = Student.query.filter_by(sname='张飞').first()
    # 查询python基础的信息
    cour = Course.query.filter_by(cname='PYTHON 基础').first()
    # 将 cour 课程追加到 stu 的 courses 列表中
    stu.courses.append(cour)
    db.session.add(stu)
    return "Add OK"

@app.route('/query_student_course')
def query_student_course():
    student = Student.query.filter_by(id=5).first()
    courses = student.courses.all()
    print('学员姓名 : %s' % student.sname)
    for cour in courses:
        print("所选课程 : %s" % cour.cname)
    return "Query OK"


if __name__ == '__main__':
    app.run(debug=True)