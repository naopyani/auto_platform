#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 定义蓝图
from flask import Blueprint

home = Blueprint("home", __name__)

import app.home.views