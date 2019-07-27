#!/usr/bin/python
#coding:utf-8

import LogCode
import unittest
import tools
import os
import traceback

from tools import PrintTip

class A000_Tool_Logcode_Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.strRunDir = os.getcwd()
        self.strTestDir = self.strRunDir + "/debug/log/" # ./debug/log/mtf.log
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
        testLog = LogCode.LogCode(self.strLogName , self.strLogFile)
        testLog.SetLevel(1)
        testLog.LogDebug(strNowDateTime + "[LogCode]test=>debug")
        testLog.LogInfo(strNowDateTime + "[LogCode]test=>info")
        testLog.LogError(strNowDateTime + "[LogCode]test=>error")
        testLog.LogCritical(strNowDateTime + "[LogCode]test=>critical")
    def testLogVerify(self):
        try:
            fdLog = open(self.strLogFile , "r")
            strLog = fdLog.read()
            if strLog.find("[LogCode]test=>critical") == 1:
                PrintTip("Can't find \"[LogCode]test=>critical\" in " + self.strLogFile)
                self.assertTrue(False)
            else:
                PrintTip("Test LogCode calss Successfule >_<")
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
#            os.remove(self.strLogFile)
        except:
            PrintTip(traceback.format_exc())            
