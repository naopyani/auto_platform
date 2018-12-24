#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from datetime import datetime
from app import db


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


if __name__ == "__main__":
    # db.create_all()
    # db.drop_all()
    # 测试数据的插入
    #
    # role = Role(
    #     name="超级管理员",
    #     auths=""
    # )
    # db.session.add(role)
    # db.session.commit()
    from werkzeug.security import generate_password_hash

    admin = User(
        name="admin",
        pwd=generate_password_hash("123456"),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
