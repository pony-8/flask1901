import os
import sys
import click

from flask import Flask,render_template,flash,redirect,request,url_for
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

app.config['SECRET_KEY'] = 'watchlist_dev'


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

#首页
@app.route('/',methods=['GET','POST'])
# @app.route('/index')
# @app.route('/home')

def index():

    # user = User.query.first()
    if request.method == 'POST':
        #request在请求触发的时候才会包含数据
        title = request.form.get('title')
        year = request.form.get('year')
        #验证数据符不符合要求
        if not title or not year or len(year)>4 or len(title)>60:
            flash('不能为空或最大长度')
            return redirect(url_for('index'))
        
        #保存表单数据
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('创建成功')

        return redirect(url_for('index'))

    movies = Movie.query.all()

    return render_template('index.html',movies=movies)

#编辑页面
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        #验证数据符不符合要求
        if not title or not year or len(year)>4 or len(title)>60:
            flash('不能为空或最大长度')
            return redirect(url_for('index'))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash("更新完成")
        return redirect(url_for('index'))

    return render_template('edit.html',movie=movie)

# 删除
@app.route('/movie/delete/<int:movie_id>',methods=['GET','POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除完成")
    return redirect(url_for('index'))



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



     
