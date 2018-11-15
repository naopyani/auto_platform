#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from flask import Flask
app = Flask(__name__)



# 不要在生成db之前导入注册蓝图。

from app.home import home as home_blueprint
app.register_blueprint(home_blueprint)
