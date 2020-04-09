from watchlistapp import app
from flask import render_template
from watchlistapp.models import User

# 错误处理函数
@app.errorhandler(404)
def page_not_found(a):
    # user = User.query.first()
    # 返回模板和状态码
    # return render_template('404.html',user=user),404
    return render_template('404.html')

