#!/usr/bin/python
#coding:utf-8

class SqlCtrlException(Exception):
    def __init__(self , _strTableName , _strMethod , _strIssueDesc):
        self.strTableName = _strTableName
        self.strMethod = _strMethod
        self.strIssueDesc = _strIssueDesc
    def __str__(self):
        return"TableName=%s,Method=%s,IssueDesc=%s" % (self.strTableName , self.strMethod , self.strIssueDesc)


