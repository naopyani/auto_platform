#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 定义蓝图
from flask import Blueprint

tree_api = Blueprint("tree_api", __name__)

import app.tree_api.posts
