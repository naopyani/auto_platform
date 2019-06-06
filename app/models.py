#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from datetime import datetime
from app import db
from flask import url_for
from app.exception import TreeApiException


# 角色
class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 角色权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    users = db.relationship("models.User")  # 管理员外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name


# 用户数据模型
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 账号
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间

    # 重构__repr__方法后，不管直接输出对象还是通过print打印的信息都按我们__repr__方法中定义的格式进行显示了
    def __repr__(self):
        return '<User %r>' % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 定义树状图模型
class Tree(db.Model):
    __tablename__ = "tree"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    pid = db.Column(db.Integer)  # 节点id
    name = db.Column(db.String(100))  # 节点名称
    is_parent = db.Column(db.Boolean)  # 是否为父节点
    loc_path = db.Column(db.String(500), unique=True)  # 节点路径
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    # 重构__repr__方法后，不管直接输出对象还是通过print打印的信息都按我们__repr__方法中定义的格式进行显示了
    def __repr__(self):
        return '<Tree %r>' % self.name

    # 所有 url_for() 方法都指定了参数 _external=True，
    # 这么做是为了生成完整的 URL，而不是生成传统 Web 程序中经常使用的
    # 相对 URL。
    def to_json(self):
        json_post = {
            'url': url_for("tree_api.get_post", loc_path=self.loc_path, _external=True),
            'id': self.id,
            'pid': self.pid,
            'name': self.name,
            'is_parent': self.is_parent,
            'loc_path': self.loc_path
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        ids = json_post.get('id')
        pid = json_post.get('pid')
        name = json_post.get('name')
        is_parent = json_post.get('is_parent')
        loc_path = json_post.get('loc_path')
        if ids is None or ids == '':
            raise TreeApiException("节点id不能为空！")
        if pid is None or pid == '':
            raise TreeApiException("节点pid不能为空！")
        if name is None or name == '':
            raise TreeApiException("名字不能为空！")
        if is_parent is None or is_parent == '':
            raise TreeApiException("是否为父节点不能为空！")
        if loc_path is None or loc_path == '':
            raise TreeApiException("当前目录不能为空！")
        return Tree(id=ids, pid=pid, name=name, is_parent=is_parent, loc_path=loc_path)


# 定义树状图id
class TreeId(db.Model):
    __tablename__ = "tree_id"
    __table_args__ = {"useexisting": True}
    tree_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<TreeId %r>' % self.tree_id

    def to_json(self):
        json_post = {'id': self.tree_id}
        return json_post


# 定义操作模型
class Oper(db.Model):
    __tablename__ = "oper"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    oper = db.Column(db.String(100))  # 动作
    oper_action = db.relationship("models.OperAction")  # 外键关系关联

    def __repr__(self):
        return '<Oper %r>' % self.oper


class OperAction(db.Model):
    __tablename__ = "oper_action"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    oper_action = db.Column(db.String(100))  # 动作类型
    param = db.Column(db.String(200))  # 所需参数
    oper_id = db.Column(db.Integer, db.ForeignKey('oper.id'))  # 操作

    def __repr__(self):
        return '<OperAction %r>' % self.oper_action


class Style(db.Model):
    __tablename__ = "style"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(100))  # 动作类型

    def __repr__(self):
        return '<Style %r>' % self.style


class KeyCode(db.Model):
    __tablename__ = "key_code"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    code_style = db.Column(db.String(100))  # 键值类型
    code_value = db.Column(db.String(100))  # 键值
    explain = db.Column(db.String(100))  # 说明

    def __repr__(self):
        return '<Style %r>' % self.style


if __name__ == "__main__":
    db.create_all()
    # db.drop_all()
    # 测试数据的插入
    #
    # role = Role(
    #     name="超级管理员",
    #     auths=""
    # )
    # db.session.add(role)
    # db.session.commit()
    # from werkzeug.security import generate_password_hash
    #
    # admin = User(
    #     name="admin",
    #     pwd=generate_password_hash("123456"),
    #     is_super=0,
    #     role_id=1
    # )
    # db.session.add(admin)
    # db.session.commit()
    # tree = Tree(
    #     id=0,
    #     pid=0,
    #     name="auto",
    #     is_parent=True,
    #     loc_path="auto/"
    # )
    # db.session.add(tree)
    # db.session.commit()
    # tree_id = TreeId(tree_id=1)
    # db.session.add(tree_id)
    # db.session.commit()
    # post = TreeId.query.first_or_404()
    # print(post.tree_id)
    # edit_data = db.session.query(TreeId).filter_by().first()
    # print(edit_data)
    # tree_list = []
    # tree = Tree.query.all()
    # for _tree in tree:
    #     every_tree = {}
    #     every_tree['id'] = _tree.id
    #     every_tree['pId'] = _tree.pid
    #     every_tree['name'] = _tree.name
    #     every_tree['is_parent'] = _tree.is_parent
    #     every_tree['loc_path'] = _tree.loc_path
    #     if _tree.pid == 0:
    #         every_tree['open'] = False
    #     tree_list.append(every_tree)
    # print(tree_list)
    # tree_node = Tree.query.filter_by(id=1).first()
    # print(tree_node)
