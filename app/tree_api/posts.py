#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# https://www.cnblogs.com/jinjidedale/p/6774266.html
# tree树状目录api接口定义
from flask import jsonify, request
from . import tree_api
from app import db
from app.models import Tree, TreeId, Oper, OperAction, Style, KeyCode
from app import exception


# 获取tree资源请求
@tree_api.route("/get_post/<string:loc_path>", methods=['GET'])
def get_post(loc_path):
    post = Tree.query.get_or_404(loc_path)
    return jsonify(post.to_json())


# 获取tree_id资源请求
@tree_api.route("/get_tree_id/", methods=['GET'])
def get_tree_id():
    tree_id = db.session.query(TreeId).filter_by().first()
    return jsonify(tree_id.tree_id)


# 通过id获取loc_path
@tree_api.route("/get_loc_path/", methods=['POST'])
def get_loc_path():
    print(request.json)
    ids = request.json.get('id')
    # 获取节点对象
    del_data = db.session.query(Tree).filter_by(id=ids).first()
    if not del_data:
        raise exception.TreeApiException("节点id：" + str(ids) + "不存在!获取loc_path！")
    loc_path = del_data.loc_path
    return jsonify(loc_path)


# 新增tree节点请求
@tree_api.route("/add_tree/", methods=['POST'])
def add_tree():
    print(request.json)
    post = Tree.from_json(request.json)
    db.session.add(post)
    db.session.commit()
    # 每新增一个id自加1
    edit_data = db.session.query(TreeId).filter_by().first()
    edit_data.tree_id += 1
    db.session.commit()
    return jsonify(post.to_json())


# 修改tree节点请求
@tree_api.route("/edit_tree/", methods=['POST'])
def edit_tree():
    print(request.json)
    loc_path = request.json.get('loc_path')
    name = request.json.get('name')
    # 获取节点对象
    edit_data = db.session.query(Tree).filter_by(loc_path=loc_path).first()
    if not edit_data:
        exception.TreeApiException("节点目录：" + str(loc_path) + "不存在!")
    # 修改节点信息
    edit_data.name = name
    db.session.commit()
    return jsonify("修改成功！")


# 删除tree节点请求
@tree_api.route("/del_tree/", methods=['GET', 'POST'])
def del_tree():
    print(request.json)
    ids = request.json.get('id')
    # 获取节点对象
    del_data = db.session.query(Tree).filter_by(id=ids).first()
    if not del_data:
        raise exception.TreeApiException("节点id：" + str(ids) + "不存在!无法删除！")
    db.session.delete(del_data)
    db.session.commit()
    return jsonify("删除成功！")


# 获取数据库的tree节点
@tree_api.route("/get_tree/", methods=['GET'])
def get_tree():
    tree_list = []
    tree = Tree.query.all()
    for _tree in tree:
        every_tree = {}
        every_tree['id'] = _tree.id
        every_tree['pId'] = _tree.pid
        every_tree['name'] = _tree.name
        every_tree['isParent'] = _tree.is_parent
        if _tree.pid == 0:
            every_tree['open'] = True
        tree_list.append(every_tree)
    print(tree_list)
    return jsonify(tree_list)


# 获取数据库的oper
@tree_api.route("/get_oper/", methods=['GET'])
def get_oper():
    oper_list = []
    oper = Oper.query.all()
    for _oper in oper:
        oper_list.append(_oper.oper)
    print(oper_list)
    return jsonify(oper_list)


# 获取数据库的oper_action
@tree_api.route("/get_oper_action/", methods=['POST'])
def get_oper_action():
    oper_action_list = []
    print(request.json)
    ids = 1
    name = request.json.get('name')
    oper_dict = {"oper": 1, "action": 2, "keyboard": 3, "assert": 4, "cal": 5}
    for key, value in oper_dict.items():
        if name in key:
            ids = value
            break
    oper_action_data = db.session.query(OperAction).filter_by(oper_id=ids).all()
    if not oper_action_data:
        raise exception.TreeApiException("此操作id：" + str(ids) + "不存在!")
    for _oper in oper_action_data:
        oper_action_tuple = (_oper.oper_action, _oper.param)
        oper_action_list.append(oper_action_tuple)
    print(oper_action_list)
    return jsonify(oper_action_list)

# 获取数据库的style
@tree_api.route("/get_style/", methods=['GET'])
def get_style():
    style_list = []
    style = Style.query.all()
    for _style in style:
        style_list.append(_style.style)
    print(style_list)
    return jsonify(style_list)