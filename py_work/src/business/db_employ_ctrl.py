#!/usr/bin/python
#coding:utf-8

import sys

from i_serial_sql import I_Mtf_Sql
from i_serial_sql import I_Mtf_DeSerial
from i_serial_sql import I_Mtf_SqlWhere
from ExceptionMtf import SqlCtrlException
from employ_info  import Employ_Info

class Db_Employ_Ctrl(I_Mtf_Sql , I_Mtf_SqlWhere , I_Mtf_DeSerial):
    strTableName = "employee"
    strSelect = "select id,name,nickname,birthday,contact1,contact2,homeaddress,workaddress,jobtype,salarytype from " + Db_Employ_Ctrl.strTableName + " where 1=1 "
    strDelete = "delete from " + Db_Employ_Ctrl.strTableName + " where id='%s' "
    strUpdate = "update " + Db_Employ_Ctrl.strTableName + " set id='%s',name='%s',nickname='%s',birthday='%s',contact1='%s',contact2='%s',homeaddress='%s',workaddress='%s',jobtype=%d,salarytype=%d where id='%s' "
    strSelCnt = "select count(1) from " + Db_Employ_Ctrl.strTableName + " limit %d offset %d where 1=1 "
    strInsert = "insert into " + Db_Employ_Ctrl.strTableName + "(id,name,nickname,birthday,contact1,contact2,homeaddress,workaddress,jobtype,salarytype) values('%s','%s','%s','%s','%s','%s','%s','%s',%d,%d) "
    def __init__(self):
        self.m_EmployInfo = None
        self.strSqlWhere = ""
    def SelectByCond(self , _objWhere = None):
        return Db_Employ_Ctrl.strSelect + self.toWhereStr()
    def DeleteByCond(self , _objWhere = None): # 必须根据Id删除，不能进行批量删除
        self.EmployInfoIdCheck(sys._getframe().f_code.co_name)
        return Db_Employ_Ctrl.strDelete % self.m_EmployInfo.strEmpolyId + self.toWhereStr()
    def UpdateByCond(self , _objWhere = None):
        self.EmployInfoIdCheck(sys._getframe().f_code.co_name)
        return Db_Employ_Ctrl.strUpdate % tuple(self.m_EmployInfo.toStrList) + self.toWhereStr()
    def InsertByCond(self , _objWhere = None):
	self.EmployInfoIdCheck(sys._getframte().f_code.co_name)
        return Db_Employ_Ctrl.strInsert % tuple(self.m_EmployInfo.toStrList) + self.toWhereStr()
    def QryCountByCond(self , _objWhere = None): # 查询总量
        return Db_Employ_Ctrl.strSelCnt + self.toWhereStr()
    def SelectByPage(iPage , iPageCount = 10): # 分页查询
        iOffset = (iPage - 1) * iPageCount
        return Db_Employ_Ctrl.strSelCnt % (iPageCount , iOffset) + self.toWhereStr()
    def DbRes2Info(_objDbRes):  # 将数据库结果集转换为Employ_Info对象，并没有安全性检查
        self.m_EmployInfo = Employ_Info(_objDbRes)
    def toWhereStr(self): # SQL语句的约束
        return self.strSqlWhere 
    def EmployInfoIdCheck(self , _strMethod):
        if self.m_EmployInfo is None :
            raise SqlCtrlException(Db_Employ_Ctrl.strTableName , _strMethod , "the None object")
        elif len(self.m_EmployInfo.strEmpolyId) == 0:
            raise SqlCtrlException(Db_Employ_Ctrl.strTableName , _strMethod , "the object id is null")
    def AddNameConstraint(self , _strName):
        self.strSqlWhere = self.strSqlWhere + " and name='%s'" % _strName
    def AddBirthdayConstraint(self , _strBegDT , _strEndDT):
        self.strSqlWhere = self.strSqlWhere + " and birthday > '%s' and birthday < '%s'" % (_strBegDT , _strEndDT)
    
