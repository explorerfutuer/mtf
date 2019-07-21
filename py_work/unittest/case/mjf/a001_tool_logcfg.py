#!/usr/bin/python
#coding:utf-8

import LogCfg
import unittest
import tools
import os
import traceback

from tools import PrintTip

class A001_Tool_Logcfg_Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.strRunDir = os.getcwd()
        self.strTestDir = self.strRunDir + "/debug/log/"  # ./debug/log/mtf.log
        self.strCfgPath = self.strRunDir + "/../bin/cfgmtf/log.json"
        self.strLogFile = self.strTestDir + "mtf.log" 
        self.strLogName = "MTF"
        try:
            os.remove(self.strLogFile)
        except FileNotFoundError:
            pass
        try:
            os.makedirs(self.strTestDir)
        except FileExistsError:
            pass
    def testLogPrint(self):
        strNowDateTime = tools.NowOffset(0)
        testLog = LogCfg.LogCfg(self.strLogName , self.strCfgPath)
        testLog.LogDebug(strNowDateTime + "[LogCfg]test=>debug")
        testLog.LogInfo(strNowDateTime + "[LogCfg]test=>LogCfginfo")
        testLog.LogError(strNowDateTime + "[LogCfg]test=>error")
        testLog.LogCritical(strNowDateTime + "[LogCfg]test=>critical")
    def testLogVerify(self):
        try:
            fdLog = open(self.strLogFile , "r")
            strLog = fdLog.read()
            if strLog.find("[LogCfg]test=>critical") == 1:
                PrintTip("Can't find \"[LogCfg]test=>critical\" in " + self.strLogFile)
                self.assertTrue(False)
            else:
                PrintTip("Test LogCfg calss Successfule >_<")
            fdLog.close()
        except :
            PrintTip(traceback.format_exc())
            self.assertTrue(False)
    def testRun(self):
        self.testLogPrint()
        self.testLogVerify()
    @classmethod
    def tearDown(self):
        try:
            os.chdir(self.strRunDir)
            os.remove(self.strLogFile)
        except:
            PrintTip(traceback.format_exc())
