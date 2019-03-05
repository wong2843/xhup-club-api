# -*- coding: utf-8 -*-
from sqlalchemy import UniqueConstraint

from app import db


"""
通用的文字编码表
"""


class CharsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False, unique=True)

    # 所属的拆字表版本号，应使用 pkg_resources.parse_version 做比较
    version = db.Column(db.String(20), index=True, nullable=False)

    # 拆字表所属群组，只有该群管理员可编辑该表
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), index=True, nullable=False)

    # 同一张拆字表的同一个版本号只能使用一次
    __table_args__ = (UniqueConstraint('name', 'version'),)

    def __repr__(self):
        return "<Chars Table '{}'>".format(self.name)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    char = db.Column(db.String(6), index=True, nullable=False)  # utf-8 最长 6 字节
    codes = db.Column(db.String(64))  # 可用编码，用空格分隔
    split = db.Column(db.String(200))  # 单字的拆分
    other_info = db.Column(db.String(200))  # 其他拆分信息，对小鹤音形来说，这是"首末编码"信息

    # 所属的拆字表 id
    table_id = db.Column(db.Integer, db.ForeignKey('chars_table.id'), index=True, nullable=False)

    # 同一张拆字表中，同一个单字只应该有一个词条
    __table_args__ = (UniqueConstraint('table_id', 'char'),)

    def __repr__(self):
        return "<Char '{}'>".format(self.char)


