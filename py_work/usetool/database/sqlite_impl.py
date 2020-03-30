#!/usr/bin/env python
#coding:utf-8

"""
sqlite3操作
"""

import sqlite3
import traceback
from database_interface import DatabaseInterface

g_iMaxStatement = 20480

class DatabaseSqlite(DatabaseInterface):
    def __init__(self, _DbInfo, _objLog):
        self.strDbPath = _DbInfo.strHost # sqlite本地存储位置
        self.logger = _objLog
        self.handleSqlite = None
        self.handleCursor = None
        try:
            self.handleSqlite = sqlite3.connect(self.strDbPath)
            self.handleCursor = self.handleSqlite.cursor()
        except:
            self.logger.log_error("sqlite3 handle init failed", traceback.format_exc())
            self.handleSqlite = None
            self.handleCursor = None
    def __del__(self):
        if self.handleSqlite is not None:
            self.handleSqlite.close()
    def start_transcation(self):
        self.handleCursor.execute("begin transaction")
    def commit(self):
        self.handleSqlite.commit() # 连接句柄进行提交
    def rollback(self):
        self.handleSqlite.rollback() # 连接句柄进行回滚
    # + list 二维数组字符串表示结果
    def query(self, _strSql):
        pass
    # + 插入失败索引列表
    def batch_insert(self, _strInsert, _listValues):
        iRetCode = 0
        listFailedIndex = []
        listIndexOffset = []
        iLenValues = len(_listValues)
        iPageSize = g_iMaxStatement / (len(_listValues[0]) + len(_listValues[-1]) + 8)  + 1
        iBathQuotients = iLenValues / iPageSize
        iBatchRemainder = iLenValues % iPageSize
        index = 1
        while index <= iBathQuotients:
            listIndexOffset.append(index * iPageSize)
            index += 1
        if iBatchRemainder != 0:
            listIndexOffset.append(iLenValues)
        # TODO批量添加
        try:
            self.handleCursor.execute("begin transaction")
            self.handleCursor.execute(_strSql)
            self.commit()
        except:
            self.rollback()
    # 自动提交执行sql
    def auto_commit_stmt(self, _strSql):
        iRetCode = 0
        try:
            self.handleCursor.execute("begin transaction")
            self.handleCursor.execute(_strSql)
            self.commit()
        except:
            self.rollback()
        return iRetCode
    # 自定义事务
    def hand_commit_stmt(self, _strSql):
        return self.execute(_strSql)
    # dml 操作
    def execute_ddl(self, _strSql):
        return self.execute(_strSql)
    def execute(self, _strSql):
        iRetCode = 0
        try:
            self.handleCursor.execute(_strSql)
        except:
            iRetCode = -1
        return iRetCode
    # todo 绑定变量形式操作
