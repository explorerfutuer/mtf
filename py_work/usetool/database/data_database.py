#!/usr/bin/env python
#coding:utf-8

"""
数据库操作类型定义
"""

class DatabaseInfo:
    def __init__(self):
        self.strHost = ""       # 主机名，IP地址
        self.iPort = 5060       # 数据库监听端口
        self.strUser = "root"   # 用户名
        self.strPassword = "root" # 用户密码
        self.strDatabase = "test" # 操作数据库
        self.mapOption = {}       # 连接数据库可选项
