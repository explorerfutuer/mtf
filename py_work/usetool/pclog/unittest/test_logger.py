#!/usr/bin/env python
#coding:utf-8

import os, sys

# 返回Python的根目录
def  LoadThirdParty(_strNodeName = "py_work/"):
    # 测试用例路径
    strPwd = os.getcwd()
    strRootDir = ""
    iPos = strPwd.find(_strNodeName)
    if iPos == -1:
        strRootDir = "../../"
    else:
        strRootDir = strPwd[:iPos] + "py_work/"
        importpath=[]
        for root , dirs , files in os.walk(strRootDir + "/usetool"):
            importpath.append(root)
            sys.path.append(root)
    return strRootDir
g_strRootDir = LoadThirdParty()

import unittest
import traceback
from logger import *

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.strCfgLog = g_strRootDir + "/bin/cfg/log.json"
        self.logger = Logger("UT" , self.strCfgLog)
    def tearDown(self):
        try:
            os.remove(self.logger.strLogFile)
        except FileExistsError:
            pass
    def test_logger_debug(self):
        strDebug = "debug debug debug >_<"
        self.logger.log_debug(strDebug)
        strLogData = ""
        try:
            with open(self.logger.strLogFile , "r") as fdTest:
                strLogFile = fdTest.read()
        except :
            print("open log file" , self.logger.strLogFile , " failed")
            self.assertTrue(False)
        self.assertNotEqual(-1 , strLogData.find(strLogData))
if __name__ == '__main__':
    unittest.main()
        
