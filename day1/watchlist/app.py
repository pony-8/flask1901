import os
import sys
import click

from flask import Flask
from flask import render_template
#导入扩展类
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

#Windows下写法
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')

#关闭了修改模型的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#初始化扩展，传入程序实例app
db = SQLAlchemy(app)

#models.py
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

#模板上下文处理函数
@app.context_processor
def common_user():

    user = User.query.first()
    return dict(user=user)

#views.py
@app.route('/')
# @app.route('/index')
# @app.route('/home')

def index():

    user = User.query.first()
    movies = Movie.query.all()

    return render_template('index.html',movies=movies)

# # 动态url
# @app.route('/index/<name>')
# def home(name):
#     return "<h1>hello,Flask,%s</h1>" %name

#自定义指令
#新建data.db的数据库初始化命令
@app.cli.command()  #装饰器，可以注册命令
@click.option('--drop',is_flag=True,help="删除后再创建")

def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库完成")    
    
#向data.db中写入数据的命令
@app.cli.command()
def forge():
    name = "pony"
    movies = [
        { "title" : "大赢家" , "year" : "2020" },
        { "title" : "叶问四" , "year" : "2020" },
        { "title" : "唐人街探案" , "year" : "2020" },
        { "title" : "囧妈" , "year" : "2020" },
    ]

    user = User(name = name)
    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo("插入数据完成")

#错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    # user = User.query.first()
    return render_template('404.html'),404



     
