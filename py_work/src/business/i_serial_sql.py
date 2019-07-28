#!/usr/bin/python
#coding:utf-8

# 接口类

class I_Mtf_Serial:
    def toStrList(self):  # 将Info对象转换为列表字符串
        pass
# 实体对象的SQL操作
class I_Mtf_Sql:
    def SelectByCond(self , _objWhere = None):
	pass
    def DeleteByCond(self , _objWhere = None):
	pass
    def UpdateByCond(self , _objWhere = None):
	pass	
    def InsertByCond(self , _objWhere = None):
	pass
    def QryCountByCond(self , _objWhere = None): # 查询总量
	pass
    def SelectByPage(iPage , iPageCount): # 分页查询
	pass
# 将数据库结果转换为实体对象
class I_Mtf_DeSerial:
    def DbRes2Info(_objDbRes):
        pass
# 查询的where条件
class I_Mtf_SqlWhere:
    def toWhereStr(self):
        return ""
#    def CheckById(self):
#        pass
#    def CheckByName(self):
#        pass
#    def CheckByDateTime(self , _strBegDT , _strEndDT):
#        pass
#    
#
