#!/usr/bin/python
#coding:utf-8

# 数据库操作实体信息
class Qry_Res_Info:
    def __inti__(self):
        self.iStatus = 0   # 查询状态
        self.listRes = []  # 查询结果集
        self.iErrCode = 0  # 查询错误代码
        self.strErrDesc = "" # 查询错误原因

class Db_Conn_Info:
    def __init__(self):
        self.iDbPort = 3006
        self.strDbIp = "127.0.0.1"
        self.strDbCharset = "utf-8"
        self.strDbName = "perfectcloth.db"
        self.strUsrName = "mtf"
        self.strUsrPwd = "mtf"

class Cfg_Type_Db_Info:
    def __init__(self):
        self.iDbType = 0
