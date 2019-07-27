#!/usr/bin/python
#coding:utf-8


import unittest
import time
import os
from tools import PrintTip
from Db_Ctrl import Adapter_Db_Ctrl
from Db_Info import Db_Conn_Info

# 测试表 test_sqlite(userseq int , username varchar(64) , userpwd varchar(64)) ;
# insert into test_sqlite(userseq , username , userpwd) values(100 , "xiaoming" , "xiaoming")
# insert into test_sqlite(userseq , username , userpwd) values(200 , "zhangsan" , "zhangsan")
class C000_Db_Sqlite3_Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.db_conn_info = Db_Conn_Info()
        self.strDataPath = "./data/"
        try:
            os.makedirs(self.strDataPath)
        except FileExistsError:
            pass
        self.db_conn_info.strDbName = "test_func.db"
        self.dbHandle = Adapter_Db_Ctrl(self.strDataPath)
        if not self.dbHandle.Init_Db(self.db_conn_info):
            PrintTip("open db connection failed")
            self.assertTrue(False)
    def testCreate(self):
        strSql = "create table test_sqlite3(userseq int , username varchar(64) , userpwd varchar(64)) ;"
        bRet , qryRes = self.dbHandle.Qry_Sql(strSql)
        if not bRet:
            PrintTip("sql:" + strSql + " execute create table failed")
            self.assertTrue(False)
    def testInsert(self):
        strSql = "insert into test_sqlite3(userseq, username, userpwd) values(1 , \"1111\" , \"1111\");"
        bRet , qryRes = self.dbHandle.Qry_Sql(strSql)
        if not bRet:
            PrintTip("sql:" + strSql + " execute insert failed")
            self.assertTrue(False)
        strSql = "insert into test_sqlite3(userseq, username, userpwd) values(2 , \"2222\" , \"2222\");"
        bRet , qryRes = self.dbHandle.Qry_Sql(strSql)
        if not bRet:
            PrintTip("sql:" + strSql + " execute insert failed")
            self.assertTrue(False)
        pass
    def testUpdate(self):
        strSql = "update test_sqlite3 set userseq = 1111 where userseq = 1;"
        bRet , qryRes = self.dbHandle.Qry_Sql(strSql)
        if not bRet:
            PrintTip("sql:" + strSql + " execute update failed")
            self.assertTrue(False)
        pass
    def testSelect(self):
        strSql = "select userseq,username,userpwd from test_sqlite3 where userseq = 2;"
        bRet , qryRes = self.dbHandle.Qry_Sql(strSql)
        if not bRet:
            PrintTip("sql:" + strSql + " execute select failed")
            self.assertTrue(False)
        if str(qryRes.listRes[0][0]) != "2" :
            PrintTip("Qry Res not wanted")
            for lRow in qryRes.listRes:
                strRow = ""
                for strCol in lRow:
                    strRow = strRow + str(strCol) + ","
                PrintTip(strRow)
            self.assertTrue(False)
    def testTransaction(self):
        pass
    def testDrop(self):
        strSql = "drop table test_sqlite3;"
        bRet , qryRes = self.dbHandle.Qry_Sql(strSql)
        if not bRet:
            PrintTip("sql:" + strSql + " execute drop table failed")
            self.assertTrue(False)
    def testVerify(self):
        strPathDbName = self.strDataPath + self.db_conn_info.strDbName
        fdVerify = os.popen("sqlite3 " + strPathDbName + " .dump")
        strDbData = fdVerify.read()
        fdVerify.close()
        if strDbData.find("test_sqlite3") == -1:
            PrintTip("test create failed")
            self.assertTrue(False)
        if strDbData.find("2222") == -1:
            PrintTip("test insert failed")
            self.assertTrue(False)
    def testRun(self):
        self.testCreate()
        self.testInsert()
        self.testUpdate()
        self.testSelect()
        self.testVerify()
#        self.testDrop()
    @classmethod
    def tearDown(self):
        pass
