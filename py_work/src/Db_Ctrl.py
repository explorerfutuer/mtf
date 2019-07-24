#!/usr/bin/python
#coding:utf-8


import logging.config
import traceback
import sqlite3


from tools   import  LogTip
from LogMtf  import  g_Log
from Db_Info import  Qry_Res_Info
from GlobalCfg import g_strDataDir

class I_Db:
    def __init__(self):
        pass
    def Init_Conn(self , _db_conn):
        pass
    def Qry_Sql(self , _str , _auto_commit):
        pass
    def Test_Conn(self):
        return True

class Mtf_Db_Ctrl(I_Db):
    def __init__(self , _str_data_path = g_strDataDir):
        self.dbConnHandle = None
        self.dbCursor = None
        self.iMaxEachFetch = 1024 * 1024 # 每次获取结果的记录最大的记录条数
        self.strDataPath = _str_data_path
        try:
            os.makedirs(self.strDataPath)
        except FileExistsError:
            pass
    def Init_Conn(self , _db_conn):
        qry_res = Qry_Res_Info()
        try:
            self.dbConnHandle = sqlite3.connect(self.strDataPath + _db_conn.strDbName , isolation_level = None)
            self.dbCursor = self.dbConnHandle.cursor()
        except:
            g_Log.LogError("[Init_Conn]" + traceback.format_exc())
    def Qry_Sql(_str , _bind_param = None, _auto_commit = True):
        try:
            if _bind_param is not None:
                self.dbCursor.execute(_str , _bind_param)
            else:
                self.dbCursor.execute(_str)
        except:
            g_Log.LogError("[Qry_Sql] execute sql:" + _str + traceback.format_exc())
            qry_res.iStatus = -1 # 有待具体
        try:
            while True:
                listTmpRes = self.dbCursor.fetchmany(size = self.iMaxEachFetch)
                iLenRes = len(listTmpRes)
                qry_res.listRes += listTmpRes
                if iLenRes < self.iMaxEachFetch :
                    qry_res.iStatus = 0
                break
        except:
            g_Log.LogError("[Qry_Sql] fetch reuslt failed" + traceback.format_exc())
            qry_res.iStatus = -2 # 有待具体
        if _auto_commit :
            self.dbConnHandle.commit()
        return qry_res
    def __del__(self):
        if self.dbConnHandle != None:
            self.dbConnHandle.close()      
    

class Adapter_Db_Ctrl:
    def __init__(self , _strDataPath = g_strDataDir):
        self.dbHandle = None
        self.strDataPath = g_strDataDir
    def Init_Db(_db_conn , _cfg_type_db = None):
        self.dbHandle = Mtf_Db_Ctrl(_db_conn , self.strDataPath)
        if self.dbHandle.dbHandle != None:
            return True
        else:
            return False
    def Qry_Sql(_str  , _bind_param = None, _auto_commit = True):
        qryRes = self.dbHandle.Qry_Sql(_str , _bind_param , _auto_commit)
        return True , qryRes
        
