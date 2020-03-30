#!/usr/bin/env python
#coding:utf-8

"""
数据库操作接口定义
"""

class DatabaseInterface:
    """接口方法中的第一个返回值表示接口调用状态"""
    def __init__(self):
        pass
    def start_transcation(self):
        pass
    def commit(self):
        pass
    def rollback(self):
        pass
    # + list 二维数组字符串表示结果
    def query(self, _strSql):
        pass
    # + 插入失败索引列表
    def batch_insert(self, _strInsert, _listValues):
        pass
    # 自动提交执行sql
    def auto_commit_stmt(self, _strSql):
        pass
    # 自定义事务
    def hand_commit_stmt(self, _strSql):
        pass
    # 执行数据定义之类的语句
    def execute_ddl(self, _strSql):
        pass
    # todo 绑定变量形式操作
