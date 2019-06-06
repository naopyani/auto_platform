#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import os

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 用于连接数据的数据库。
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost:3306/auto_platform"
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = "cbb88e54b0ff4f03a2666a45818ffaa4"
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
app.config["FC_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users/")
app.debug = False
db = SQLAlchemy(app)

# 不要在生成db之前导入注册蓝图。

from app.home import home as home_blueprint
from app.tree_api import tree_api as tree_api_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(tree_api_blueprint, url_prefix='/tree_api')


@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("home/404.html"), 404


# 定义错误请求
def bad_request(message):
    response = jsonify({'错误': '请求错误！', '信息': message})
    response.status_code = 400
    return response


from app import exception


# 程序需要向客户端提供适当的响应以处理这个异常。为了避免在视图函数中编写捕
# 获异常的代码， 我们可创建一个全局异常处理程序。
@tree_api_blueprint.errorhandler(exception.TreeApiException)
def tree_api_error(e):
    return bad_request(e.args[0])
