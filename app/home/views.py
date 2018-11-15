#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from . import home
from flask import render_template

@home.route("/", methods=["GET"])
def index():
    render_template("home/index.html")
